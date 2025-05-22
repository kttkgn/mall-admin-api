from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from app.db.base_class import Base, TimestampMixin

class Statistics(Base, TimestampMixin):
    """统计表"""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    date = Column(DateTime, nullable=False, index=True, comment="统计日期")
    total_sales = Column(Float, default=0, comment="总销售额")
    total_orders = Column(Integer, default=0, comment="总订单数")
    total_users = Column(Integer, default=0, comment="总用户数")
    total_products = Column(Integer, default=0, comment="总商品数")
    total_refunds = Column(Integer, default=0, comment="总退款数")
    total_refund_amount = Column(Float, default=0, comment="总退款金额")
    avg_order_amount = Column(Float, default=0, comment="平均订单金额")
    conversion_rate = Column(Float, default=0, comment="转化率")
    extra = Column(JSON, comment="额外统计信息")

class SalesTrend(Base, TimestampMixin):
    """销售趋势表"""
    __tablename__ = "sales_trends"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    date = Column(DateTime, nullable=False, index=True, comment="日期")
    sales_amount = Column(Float, default=0, comment="销售额")
    order_count = Column(Integer, default=0, comment="订单数")
    user_count = Column(Integer, default=0, comment="用户数")
    product_count = Column(Integer, default=0, comment="商品数")
    refund_count = Column(Integer, default=0, comment="退款数")
    refund_amount = Column(Float, default=0, comment="退款金额")
    extra = Column(JSON, comment="额外趋势信息")

class ProductRanking(Base, TimestampMixin):
    """商品排行表"""
    __tablename__ = "product_rankings"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    product_id = Column(Integer, nullable=False, index=True, comment="商品ID")
    date = Column(DateTime, nullable=False, index=True, comment="统计日期")
    sales_amount = Column(Float, default=0, comment="销售额")
    sales_count = Column(Integer, default=0, comment="销量")
    view_count = Column(Integer, default=0, comment="浏览量")
    favorite_count = Column(Integer, default=0, comment="收藏量")
    cart_count = Column(Integer, default=0, comment="加购量")
    ranking = Column(Integer, default=0, comment="排名")
    extra = Column(JSON, comment="额外排行信息") 