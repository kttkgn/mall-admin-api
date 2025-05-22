from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.after_sale import AfterSale, AfterSaleLog
from app.models.order import Order, OrderItem
from app.schemas.after_sale import (
    AfterSaleCreate,
    AfterSaleUpdate,
    AfterSaleLogCreate,
)

def get_after_sale(db: Session, after_sale_id: int) -> Optional[AfterSale]:
    return db.query(AfterSale).filter(AfterSale.id == after_sale_id).first()

def get_after_sales(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    order_id: Optional[int] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,
) -> List[AfterSale]:
    query = db.query(AfterSale)
    if user_id is not None:
        query = query.filter(AfterSale.user_id == user_id)
    if order_id is not None:
        query = query.filter(AfterSale.order_id == order_id)
    if status is not None:
        query = query.filter(AfterSale.status == status)
    if type is not None:
        query = query.filter(AfterSale.type == type)
    return query.offset(skip).limit(limit).all()

def create_after_sale(db: Session, after_sale_in: AfterSaleCreate, user_id: int) -> AfterSale:
    # 检查订单和订单项是否存在
    order = db.query(Order).filter(Order.id == after_sale_in.order_id).first()
    order_item = db.query(OrderItem).filter(OrderItem.id == after_sale_in.order_item_id).first()
    if not order or not order_item:
        raise ValueError("订单或订单项不存在")
    
    # 检查是否已经存在售后申请
    existing = db.query(AfterSale).filter(
        AfterSale.order_item_id == after_sale_in.order_item_id,
        AfterSale.status.in_(['pending', 'approved', 'processing'])
    ).first()
    if existing:
        raise ValueError("该订单项已存在进行中的售后申请")
    
    # 创建售后申请
    db_after_sale = AfterSale(
        order_id=after_sale_in.order_id,
        order_item_id=after_sale_in.order_item_id,
        user_id=user_id,
        type=after_sale_in.type,
        reason=after_sale_in.reason,
        description=after_sale_in.description,
    )
    db.add(db_after_sale)
    
    # 创建售后日志
    db_log = AfterSaleLog(
        after_sale_id=db_after_sale.id,
        action="create",
        operator=f"user_{user_id}",
        remark="创建售后申请",
    )
    db.add(db_log)
    
    db.commit()
    db.refresh(db_after_sale)
    return db_after_sale

def update_after_sale(
    db: Session, after_sale_id: int, after_sale_in: AfterSaleUpdate, operator: str
) -> Optional[AfterSale]:
    db_after_sale = get_after_sale(db, after_sale_id)
    if not db_after_sale:
        return None
    
    update_data = after_sale_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_after_sale, field, value)
    
    # 创建售后日志
    db_log = AfterSaleLog(
        after_sale_id=after_sale_id,
        action="update",
        operator=operator,
        remark=f"更新售后状态为{after_sale_in.status}" if after_sale_in.status else "更新售后信息",
        extra=update_data,
    )
    db.add(db_log)
    
    db.add(db_after_sale)
    db.commit()
    db.refresh(db_after_sale)
    return db_after_sale

def get_after_sale_logs(
    db: Session, after_sale_id: int, skip: int = 0, limit: int = 100
) -> List[AfterSaleLog]:
    return (
        db.query(AfterSaleLog)
        .filter(AfterSaleLog.after_sale_id == after_sale_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_after_sale_log(
    db: Session, after_sale_id: int, log_in: AfterSaleLogCreate
) -> AfterSaleLog:
    db_log = AfterSaleLog(
        after_sale_id=after_sale_id,
        action=log_in.action,
        operator=log_in.operator,
        remark=log_in.remark,
        extra=log_in.extra,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log 