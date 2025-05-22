from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

# Statistics schemas
class StatisticsBase(BaseModel):
    """统计基础 schema"""
    date: datetime
    total_sales: float = 0
    total_orders: int = 0
    total_users: int = 0
    total_products: int = 0
    total_refunds: int = 0
    total_refund_amount: float = 0
    avg_order_amount: float = 0
    conversion_rate: float = 0
    extra: Optional[Dict[str, Any]] = None

class StatisticsCreate(StatisticsBase):
    """创建统计 schema"""
    pass

class StatisticsUpdate(BaseModel):
    """更新统计 schema"""
    total_sales: Optional[float] = None
    total_orders: Optional[int] = None
    total_users: Optional[int] = None
    total_products: Optional[int] = None
    total_refunds: Optional[int] = None
    total_refund_amount: Optional[float] = None
    avg_order_amount: Optional[float] = None
    conversion_rate: Optional[float] = None
    extra: Optional[Dict[str, Any]] = None

class StatisticsInDB(StatisticsBase):
    """数据库中的统计 schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Statistics(StatisticsInDB):
    """统计 schema"""
    pass

# SalesTrend schemas
class SalesTrendBase(BaseModel):
    """销售趋势基础 schema"""
    date: datetime
    sales_amount: float = 0
    order_count: int = 0
    user_count: int = 0
    product_count: int = 0
    refund_count: int = 0
    refund_amount: float = 0
    extra: Optional[Dict[str, Any]] = None

class SalesTrendCreate(SalesTrendBase):
    """创建销售趋势 schema"""
    pass

class SalesTrendUpdate(BaseModel):
    """更新销售趋势 schema"""
    sales_amount: Optional[float] = None
    order_count: Optional[int] = None
    user_count: Optional[int] = None
    product_count: Optional[int] = None
    refund_count: Optional[int] = None
    refund_amount: Optional[float] = None
    extra: Optional[Dict[str, Any]] = None

class SalesTrendInDB(SalesTrendBase):
    """数据库中的销售趋势 schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SalesTrend(SalesTrendInDB):
    """销售趋势 schema"""
    pass

# ProductRanking schemas
class ProductRankingBase(BaseModel):
    """商品排行基础 schema"""
    product_id: int
    date: datetime
    sales_amount: float = 0
    sales_count: int = 0
    view_count: int = 0
    favorite_count: int = 0
    cart_count: int = 0
    ranking: int = 0
    extra: Optional[Dict[str, Any]] = None

class ProductRankingCreate(ProductRankingBase):
    """创建商品排行 schema"""
    pass

class ProductRankingUpdate(BaseModel):
    """更新商品排行 schema"""
    sales_amount: Optional[float] = None
    sales_count: Optional[int] = None
    view_count: Optional[int] = None
    favorite_count: Optional[int] = None
    cart_count: Optional[int] = None
    ranking: Optional[int] = None
    extra: Optional[Dict[str, Any]] = None

class ProductRankingInDB(ProductRankingBase):
    """数据库中的商品排行 schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductRanking(ProductRankingInDB):
    """商品排行 schema"""
    pass

# Response schemas
class StatisticsList(BaseModel):
    """统计列表响应 schema"""
    total: int
    items: List[Statistics]

class SalesTrendList(BaseModel):
    """销售趋势列表响应 schema"""
    total: int
    items: List[SalesTrend]

class ProductRankingList(BaseModel):
    """商品排行列表响应 schema"""
    total: int
    items: List[ProductRanking]

class DashboardStats(BaseModel):
    """仪表盘统计数据模型"""
    today_sales: float  # 今日销售额
    today_orders: int  # 今日订单数
    today_users: int  # 今日新增用户
    today_refunds: int  # 今日退款数
    today_refund_amount: float  # 今日退款金额
    total_sales: float  # 总销售额
    total_orders: int  # 总订单数
    total_users: int  # 总用户数
    total_products: int  # 总商品数
    total_refunds: int  # 总退款数
    total_refund_amount: float  # 总退款金额
    avg_order_amount: float  # 平均订单金额
    conversion_rate: float  # 转化率
    sales_trend: List[SalesTrend]  # 销售趋势
    product_rankings: List[ProductRanking]  # 商品排行 