from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.models.statistics import SalesTrend, ProductRanking
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product
from app.models.after_sale import AfterSale
from app.schemas.statistics import (
    SalesTrendCreate,
    ProductRankingCreate,
    DashboardStats,
)

def get_dashboard_stats(db: Session) -> DashboardStats:
    """获取仪表盘统计数据"""
    # 获取今日开始时间
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 总销售额
    total_sales = db.query(func.sum(Order.total_amount)).filter(
        Order.status.in_(['paid', 'shipped', 'completed'])
    ).scalar() or 0
    
    # 总订单数
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    
    # 总用户数
    total_users = db.query(func.count(User.id)).scalar() or 0
    
    # 总商品数
    total_products = db.query(func.count(Product.id)).scalar() or 0
    
    # 总退款数和金额
    total_refunds = db.query(func.count(AfterSale.id)).filter(
        AfterSale.status == 'completed'
    ).scalar() or 0
    refund_amount = db.query(func.sum(AfterSale.refund_amount)).filter(
        AfterSale.status == 'completed'
    ).scalar() or 0
    
    # 今日销售额
    today_sales = db.query(func.sum(Order.total_amount)).filter(
        and_(
            Order.status.in_(['paid', 'shipped', 'completed']),
            Order.created_at >= today
        )
    ).scalar() or 0
    
    # 今日订单数
    today_orders = db.query(func.count(Order.id)).filter(
        Order.created_at >= today
    ).scalar() or 0
    
    # 今日新增用户数
    today_users = db.query(func.count(User.id)).filter(
        User.created_at >= today
    ).scalar() or 0
    
    # 今日退款数和金额
    today_refunds = db.query(func.count(AfterSale.id)).filter(
        and_(
            AfterSale.status == 'completed',
            AfterSale.complete_time >= today
        )
    ).scalar() or 0
    today_refund_amount = db.query(func.sum(AfterSale.refund_amount)).filter(
        and_(
            AfterSale.status == 'completed',
            AfterSale.complete_time >= today
        )
    ).scalar() or 0
    
    return DashboardStats(
        total_sales=total_sales,
        total_orders=total_orders,
        total_users=total_users,
        total_products=total_products,
        total_refunds=total_refunds,
        refund_amount=refund_amount,
        today_sales=today_sales,
        today_orders=today_orders,
        today_users=today_users,
        today_refunds=today_refunds,
        today_refund_amount=today_refund_amount,
    )

def get_sales_trends(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    skip: int = 0,
    limit: int = 100,
) -> List[SalesTrend]:
    """获取销售趋势数据"""
    return (
        db.query(SalesTrend)
        .filter(
            and_(
                SalesTrend.date >= start_date,
                SalesTrend.date <= end_date
            )
        )
        .order_by(SalesTrend.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_sales_trend(
    db: Session, trend_in: SalesTrendCreate
) -> SalesTrend:
    """创建销售趋势数据"""
    db_trend = SalesTrend(**trend_in.dict())
    db.add(db_trend)
    db.commit()
    db.refresh(db_trend)
    return db_trend

def get_product_rankings(
    db: Session,
    date: datetime,
    skip: int = 0,
    limit: int = 100,
) -> List[ProductRanking]:
    """获取商品排行数据"""
    return (
        db.query(ProductRanking)
        .filter(ProductRanking.date == date)
        .order_by(ProductRanking.sales_amount.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_product_ranking(
    db: Session, ranking_in: ProductRankingCreate
) -> ProductRanking:
    """创建商品排行数据"""
    db_ranking = ProductRanking(**ranking_in.dict())
    db.add(db_ranking)
    db.commit()
    db.refresh(db_ranking)
    return db_ranking 