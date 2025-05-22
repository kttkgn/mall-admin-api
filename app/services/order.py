from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order, OrderItem, OrderLog
from app.models.product import Product, ProductSKU
from app.models.user import User
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    OrderItemUpdate,
    OrderLogCreate,
    OrderLogUpdate,
)
from app import crud, models

def generate_order_no() -> str:
    """生成订单号"""
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(int(datetime.now().timestamp() * 1000))[-6:]

def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def get_order_by_no(db: Session, order_no: str) -> Optional[Order]:
    return db.query(Order).filter(Order.order_no == order_no).first()

def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
) -> List[Order]:
    query = db.query(Order)
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)
    if status is not None:
        query = query.filter(Order.status == status)
    return query.offset(skip).limit(limit).all()

def create_order(db: Session, order_in: OrderCreate, user_id: int) -> Order:
    # 创建订单
    order_no = generate_order_no()
    db_order = Order(
        order_no=order_no,
        user_id=user_id,
        total_amount=order_in.total_amount,
        receiver_name=order_in.receiver_name,
        receiver_phone=order_in.receiver_phone,
        receiver_province=order_in.receiver_province,
        receiver_city=order_in.receiver_city,
        receiver_district=order_in.receiver_district,
        receiver_address=order_in.receiver_address,
        remark=order_in.remark,
    )
    db.add(db_order)
    db.flush()  # 获取订单ID
    
    # 创建订单项
    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        sku = db.query(ProductSKU).filter(ProductSKU.id == item.sku_id).first()
        if not product or not sku:
            raise ValueError("商品或SKU不存在")
        
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            sku_id=item.sku_id,
            product_name=product.name,
            product_image=product.main_image,
            sku_code=sku.code,
            sku_attributes=sku.attributes,
            price=sku.price,
            quantity=item.quantity,
            total_amount=sku.price * item.quantity,
        )
        db.add(db_item)
    
    # 创建订单日志
    db_log = OrderLog(
        order_id=db_order.id,
        action="create",
        operator=f"user_{user_id}",
        remark="创建订单",
    )
    db.add(db_log)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(
    db: Session, order_id: int, order_in: OrderUpdate, operator: str
) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    update_data = order_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)
    
    # 创建订单日志
    db_log = OrderLog(
        order_id=order_id,
        action="update",
        operator=operator,
        remark=f"更新订单状态为{order_in.status}" if order_in.status else "更新订单信息",
        extra=update_data,
    )
    db.add(db_log)
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_logs(
    db: Session, order_id: int, skip: int = 0, limit: int = 100
) -> List[OrderLog]:
    return (
        db.query(OrderLog)
        .filter(OrderLog.order_id == order_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_order_log(
    db: Session, order_id: int, log_in: OrderLogCreate
) -> OrderLog:
    db_log = OrderLog(
        order_id=order_id,
        action=log_in.action,
        operator=log_in.operator,
        remark=log_in.remark,
        extra=log_in.extra,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

class OrderService:
    @staticmethod
    async def get_order(db: AsyncSession, order_id: int) -> Optional[Order]:
        """
        获取订单详情
        """
        result = await db.execute(select(Order).filter(Order.id == order_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_orders(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        获取订单列表
        """
        result = await db.execute(select(Order).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create_order(db: AsyncSession, order_in: OrderCreate) -> Order:
        """
        创建订单
        """
        order = Order(**order_in.dict(exclude={"items"}))
        db.add(order)
        await db.flush()

        # 创建订单项
        for item_in in order_in.items:
            item = OrderItem(**item_in.dict(), order_id=order.id)
            db.add(item)

        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def update_order(
        db: AsyncSession, order_id: int, order_in: OrderUpdate
    ) -> Optional[Order]:
        """
        更新订单
        """
        order = await OrderService.get_order(db, order_id)
        if not order:
            return None

        for field, value in order_in.dict(exclude_unset=True).items():
            setattr(order, field, value)

        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def delete_order(db: AsyncSession, order_id: int) -> bool:
        """
        删除订单
        """
        order = await OrderService.get_order(db, order_id)
        if not order:
            return False

        await db.delete(order)
        await db.commit()
        return True

    @staticmethod
    async def get_order_items(
        db: AsyncSession, order_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderItem]:
        """
        获取订单项列表
        """
        result = await db.execute(
            select(OrderItem)
            .filter(OrderItem.order_id == order_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create_order_item(
        db: AsyncSession, order_id: int, item_in: OrderItemCreate
    ) -> Optional[OrderItem]:
        """
        创建订单项
        """
        order = await OrderService.get_order(db, order_id)
        if not order:
            return None

        item = OrderItem(**item_in.dict(), order_id=order.id)
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def update_order_item(
        db: AsyncSession, order_id: int, item_id: int, item_in: OrderItemUpdate
    ) -> Optional[OrderItem]:
        """
        更新订单项
        """
        result = await db.execute(
            select(OrderItem).filter(
                OrderItem.id == item_id, OrderItem.order_id == order_id
            )
        )
        item = result.scalar_one_or_none()
        if not item:
            return None

        for field, value in item_in.dict(exclude_unset=True).items():
            setattr(item, field, value)

        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def delete_order_item(
        db: AsyncSession, order_id: int, item_id: int
    ) -> bool:
        """
        删除订单项
        """
        result = await db.execute(
            select(OrderItem).filter(
                OrderItem.id == item_id, OrderItem.order_id == order_id
            )
        )
        item = result.scalar_one_or_none()
        if not item:
            return False

        await db.delete(item)
        await db.commit()
        return True

    @staticmethod
    async def get_order_logs(
        db: AsyncSession, order_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderLog]:
        """
        获取订单日志列表
        """
        result = await db.execute(
            select(OrderLog)
            .filter(OrderLog.order_id == order_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create_order_log(
        db: AsyncSession, order_id: int, log_in: OrderLogCreate
    ) -> Optional[OrderLog]:
        """
        创建订单日志
        """
        order = await OrderService.get_order(db, order_id)
        if not order:
            return None

        log = OrderLog(**log_in.dict(), order_id=order.id)
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

order_service = OrderService() 