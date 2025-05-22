from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem, OrderLog
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate, OrderLogCreate
import uuid


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    async def get_by_order_no(self, db: AsyncSession, *, order_no: str) -> Optional[Order]:
        """
        通过订单号获取订单
        """
        result = await db.execute(select(Order).filter(Order.order_no == order_no))
        return result.scalar_one_or_none()

    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        获取用户的订单列表
        """
        result = await db.execute(
            select(Order)
            .filter(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_with_items(
        self, db: AsyncSession, *, obj_in: OrderCreate, user_id: int
    ) -> Order:
        """
        创建订单及其订单项
        """
        # 生成订单号
        order_no = f"ORDER{uuid.uuid4().hex[:8].upper()}"
        
        # 创建订单
        order_data = obj_in.dict(exclude={"items"})
        order_data["order_no"] = order_no
        order_data["user_id"] = user_id
        db_obj = Order(**order_data)
        db.add(db_obj)
        await db.flush()
        
        # 创建订单项
        total_amount = 0
        for item in obj_in.items:
            item_data = item.dict()
            item_data["order_id"] = db_obj.id
            db_item = OrderItem(**item_data)
            db.add(db_item)
            total_amount += item_data["price"] * item_data["quantity"]
        
        # 更新订单总金额
        db_obj.total_amount = total_amount
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, OrderItemCreate]):
    async def get_by_order(
        self, db: AsyncSession, *, order_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderItem]:
        """
        获取订单的订单项列表
        """
        result = await db.execute(
            select(OrderItem)
            .filter(OrderItem.order_id == order_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDOrderLog(CRUDBase[OrderLog, OrderLogCreate, OrderLogCreate]):
    async def get_by_order(
        self, db: AsyncSession, *, order_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderLog]:
        """
        获取订单的日志列表
        """
        result = await db.execute(
            select(OrderLog)
            .filter(OrderLog.order_id == order_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


order = CRUDOrder(Order)
order_item = CRUDOrderItem(OrderItem)
order_log = CRUDOrderLog(OrderLog) 