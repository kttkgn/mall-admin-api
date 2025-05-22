from typing import Any, Dict, List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.after_sale import AfterSale, AfterSaleItem, AfterSaleLog
from app.schemas.after_sale import (
    AfterSaleCreate,
    AfterSaleUpdate,
    AfterSaleItemCreate,
    AfterSaleItemUpdate,
    AfterSaleLogCreate,
    AfterSaleLogUpdate,
)


class CRUDAfterSale(CRUDBase[AfterSale, AfterSaleCreate, AfterSaleUpdate]):
    async def get_by_order(
        self, db: AsyncSession, *, order_id: int, skip: int = 0, limit: int = 100
    ) -> List[AfterSale]:
        """
        获取指定订单的售后列表
        """
        result = await db.execute(
            select(AfterSale)
            .filter(AfterSale.order_id == order_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[AfterSale]:
        """
        获取指定用户的售后列表
        """
        result = await db.execute(
            select(AfterSale)
            .filter(AfterSale.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDAfterSaleItem(CRUDBase[AfterSaleItem, AfterSaleItemCreate, AfterSaleItemUpdate]):
    async def get_by_after_sale(
        self, db: AsyncSession, *, after_sale_id: int, skip: int = 0, limit: int = 100
    ) -> List[AfterSaleItem]:
        """
        获取指定售后单的商品列表
        """
        result = await db.execute(
            select(AfterSaleItem)
            .filter(AfterSaleItem.after_sale_id == after_sale_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDAfterSaleLog(CRUDBase[AfterSaleLog, AfterSaleLogCreate, AfterSaleLogUpdate]):
    async def get_by_after_sale(
        self, db: AsyncSession, *, after_sale_id: int, skip: int = 0, limit: int = 100
    ) -> List[AfterSaleLog]:
        """
        获取指定售后单的日志列表
        """
        result = await db.execute(
            select(AfterSaleLog)
            .filter(AfterSaleLog.after_sale_id == after_sale_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


after_sale = CRUDAfterSale(AfterSale)
after_sale_item = CRUDAfterSaleItem(AfterSaleItem)
after_sale_log = CRUDAfterSaleLog(AfterSaleLog) 