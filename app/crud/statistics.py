from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.statistics import Statistics, SalesTrend, ProductRanking
from app.schemas.statistics import (
    StatisticsCreate,
    StatisticsUpdate,
    SalesTrendCreate,
    SalesTrendUpdate,
    ProductRankingCreate,
    ProductRankingUpdate,
)


class CRUDStatistics(CRUDBase[Statistics, StatisticsCreate, StatisticsUpdate]):
    async def get_by_date(
        self, db: AsyncSession, *, date: datetime, skip: int = 0, limit: int = 100
    ) -> List[Statistics]:
        """
        获取指定日期的统计数据
        """
        result = await db.execute(
            select(Statistics)
            .filter(Statistics.date == date)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_date_range(
        self, db: AsyncSession, *, start_date: datetime, end_date: datetime
    ) -> List[Statistics]:
        """
        获取日期范围内的统计数据
        """
        result = await db.execute(
            select(Statistics)
            .filter(Statistics.date >= start_date)
            .filter(Statistics.date <= end_date)
            .order_by(Statistics.date)
        )
        return result.scalars().all()


class CRUDSalesTrend(CRUDBase[SalesTrend, SalesTrendCreate, SalesTrendUpdate]):
    async def get_by_date(
        self, db: AsyncSession, *, date: datetime, skip: int = 0, limit: int = 100
    ) -> List[SalesTrend]:
        """
        获取指定日期的销售趋势数据
        """
        result = await db.execute(
            select(SalesTrend)
            .filter(SalesTrend.date == date)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_date_range(
        self, db: AsyncSession, *, start_date: datetime, end_date: datetime
    ) -> List[SalesTrend]:
        """
        获取日期范围内的销售趋势数据
        """
        result = await db.execute(
            select(SalesTrend)
            .filter(SalesTrend.date >= start_date)
            .filter(SalesTrend.date <= end_date)
            .order_by(SalesTrend.date)
        )
        return result.scalars().all()


class CRUDProductRanking(CRUDBase[ProductRanking, ProductRankingCreate, ProductRankingUpdate]):
    async def get_by_date(
        self, db: AsyncSession, *, date: datetime, skip: int = 0, limit: int = 100
    ) -> List[ProductRanking]:
        """
        获取指定日期的商品排行数据
        """
        result = await db.execute(
            select(ProductRanking)
            .filter(ProductRanking.date == date)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_product(
        self, db: AsyncSession, *, product_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProductRanking]:
        """
        获取指定商品的排行数据
        """
        result = await db.execute(
            select(ProductRanking)
            .filter(ProductRanking.product_id == product_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


statistics = CRUDStatistics(Statistics)
sales_trend = CRUDSalesTrend(SalesTrend)
product_ranking = CRUDProductRanking(ProductRanking) 