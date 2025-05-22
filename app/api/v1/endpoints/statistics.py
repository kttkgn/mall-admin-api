from typing import Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services import statistics as statistics_service

router = APIRouter()

@router.get("/dashboard", response_model=schemas.DashboardStats)
def read_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    获取仪表盘统计数据
    """
    return statistics_service.get_dashboard_stats(db)

@router.get("/sales-trends", response_model=schemas.SalesTrendList)
def read_sales_trends(
    db: Session = Depends(deps.get_db),
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    获取销售趋势数据
    """
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    trends = statistics_service.get_sales_trends(
        db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
    )
    total = db.query(models.SalesTrend).filter(
        models.SalesTrend.date.between(start_date, end_date)
    ).count()
    return {"total": total, "items": trends}

@router.post("/sales-trends", response_model=schemas.SalesTrend)
def create_sales_trend(
    *,
    db: Session = Depends(deps.get_db),
    trend_in: schemas.SalesTrendCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    创建销售趋势数据
    """
    trend = statistics_service.create_sales_trend(db, trend_in)
    return trend

@router.get("/product-rankings", response_model=schemas.ProductRankingList)
def read_product_rankings(
    db: Session = Depends(deps.get_db),
    date: datetime = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    获取商品排行数据
    """
    if not date:
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    rankings = statistics_service.get_product_rankings(
        db, date=date, skip=skip, limit=limit
    )
    total = db.query(models.ProductRanking).filter(
        models.ProductRanking.date == date
    ).count()
    return {"total": total, "items": rankings}

@router.post("/product-rankings", response_model=schemas.ProductRanking)
def create_product_ranking(
    *,
    db: Session = Depends(deps.get_db),
    ranking_in: schemas.ProductRankingCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    创建商品排行数据
    """
    ranking = statistics_service.create_product_ranking(db, ranking_in)
    return ranking 