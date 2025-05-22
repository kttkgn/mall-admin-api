from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product
from app.models.after_sale import AfterSale
from app.models.statistics import SalesTrend, ProductRanking
from app.schemas.statistics import SalesTrendCreate, ProductRankingCreate

def generate_daily_statistics():
    """生成每日统计数据"""
    db = SessionLocal()
    try:
        # 获取昨天的日期
        yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        # 生成销售趋势数据
        generate_sales_trend(db, yesterday)
        
        # 生成商品排行数据
        generate_product_rankings(db, yesterday)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def generate_sales_trend(db: Session, date: datetime):
    """生成销售趋势数据"""
    # 检查是否已存在当天的数据
    existing = db.query(SalesTrend).filter(SalesTrend.date == date).first()
    if existing:
        return
    
    # 计算销售额
    total_sales = db.query(func.sum(Order.total_amount)).filter(
        and_(
            Order.status.in_(['paid', 'shipped', 'completed']),
            Order.created_at >= date,
            Order.created_at < date + timedelta(days=1)
        )
    ).scalar() or 0
    
    # 计算订单数
    order_count = db.query(func.count(Order.id)).filter(
        and_(
            Order.created_at >= date,
            Order.created_at < date + timedelta(days=1)
        )
    ).scalar() or 0
    
    # 计算新增用户数
    user_count = db.query(func.count(User.id)).filter(
        and_(
            User.created_at >= date,
            User.created_at < date + timedelta(days=1)
        )
    ).scalar() or 0
    
    # 计算退款金额和数量
    refund_amount = db.query(func.sum(AfterSale.refund_amount)).filter(
        and_(
            AfterSale.status == 'completed',
            AfterSale.complete_time >= date,
            AfterSale.complete_time < date + timedelta(days=1)
        )
    ).scalar() or 0
    refund_count = db.query(func.count(AfterSale.id)).filter(
        and_(
            AfterSale.status == 'completed',
            AfterSale.complete_time >= date,
            AfterSale.complete_time < date + timedelta(days=1)
        )
    ).scalar() or 0
    
    # 创建销售趋势数据
    trend_in = SalesTrendCreate(
        date=date,
        total_sales=total_sales,
        order_count=order_count,
        user_count=user_count,
        refund_amount=refund_amount,
        refund_count=refund_count,
    )
    db_trend = SalesTrend(**trend_in.dict())
    db.add(db_trend)

def generate_product_rankings(db: Session, date: datetime):
    """生成商品排行数据"""
    # 检查是否已存在当天的数据
    existing = db.query(ProductRanking).filter(ProductRanking.date == date).first()
    if existing:
        return
    
    # 获取所有商品
    products = db.query(Product).all()
    
    for product in products:
        # 计算销售额
        sales_amount = db.query(func.sum(OrderItem.total_amount)).filter(
            and_(
                OrderItem.product_id == product.id,
                OrderItem.created_at >= date,
                OrderItem.created_at < date + timedelta(days=1)
            )
        ).scalar() or 0
        
        # 计算销售数量
        sales_count = db.query(func.sum(OrderItem.quantity)).filter(
            and_(
                OrderItem.product_id == product.id,
                OrderItem.created_at >= date,
                OrderItem.created_at < date + timedelta(days=1)
            )
        ).scalar() or 0
        
        # 创建商品排行数据
        ranking_in = ProductRankingCreate(
            date=date,
            product_id=product.id,
            product_name=product.name,
            sales_amount=sales_amount,
            sales_count=sales_count,
            view_count=0,  # 需要另外统计
        )
        db_ranking = ProductRanking(**ranking_in.dict())
        db.add(db_ranking) 