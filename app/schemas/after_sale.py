from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

# AfterSale schemas
class AfterSaleBase(BaseModel):
    """售后基础 schema"""
    type: str  # refund, return, exchange
    reason: str
    description: Optional[str] = None

class AfterSaleCreate(AfterSaleBase):
    """创建售后 schema"""
    order_id: int
    order_item_id: int
    items: List["AfterSaleItemCreate"]

class AfterSaleUpdate(BaseModel):
    """更新售后 schema"""
    status: Optional[str] = None
    refund_amount: Optional[float] = None
    reject_reason: Optional[str] = None
    return_tracking_no: Optional[str] = None
    return_company: Optional[str] = None
    exchange_tracking_no: Optional[str] = None
    exchange_company: Optional[str] = None

class AfterSaleInDB(AfterSaleBase):
    """数据库中的售后 schema"""
    id: int
    order_id: int
    order_item_id: int
    user_id: int
    status: str
    refund_amount: Optional[float]
    refund_time: Optional[datetime]
    reject_reason: Optional[str]
    reject_time: Optional[datetime]
    complete_time: Optional[datetime]
    cancel_time: Optional[datetime]
    cancel_reason: Optional[str]
    return_tracking_no: Optional[str]
    return_company: Optional[str]
    return_time: Optional[datetime]
    exchange_tracking_no: Optional[str]
    exchange_company: Optional[str]
    exchange_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    items: List["AfterSaleItem"]

    class Config:
        from_attributes = True

class AfterSale(AfterSaleInDB):
    """售后 schema"""
    pass

# AfterSaleItem schemas
class AfterSaleItemBase(BaseModel):
    """售后商品基础 schema"""
    product_id: int
    product_sku_id: int
    quantity: int
    price: float
    refund_amount: Optional[float] = None
    reason: Optional[str] = None

class AfterSaleItemCreate(AfterSaleItemBase):
    """创建售后商品 schema"""
    pass

class AfterSaleItemUpdate(BaseModel):
    """更新售后商品 schema"""
    quantity: Optional[int] = None
    price: Optional[float] = None
    refund_amount: Optional[float] = None
    reason: Optional[str] = None

class AfterSaleItemInDB(AfterSaleItemBase):
    """数据库中的售后商品 schema"""
    id: int
    after_sale_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AfterSaleItem(AfterSaleItemInDB):
    """售后商品 schema"""
    pass

# AfterSaleLog schemas
class AfterSaleLogBase(BaseModel):
    """售后日志基础 schema"""
    action: str
    operator: str
    remark: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class AfterSaleLogCreate(AfterSaleLogBase):
    """创建售后日志 schema"""
    after_sale_id: int

class AfterSaleLogUpdate(BaseModel):
    """更新售后日志 schema"""
    action: Optional[str] = None
    operator: Optional[str] = None
    remark: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class AfterSaleLogInDB(AfterSaleLogBase):
    """数据库中的售后日志 schema"""
    id: int
    after_sale_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AfterSaleLog(AfterSaleLogInDB):
    """售后日志 schema"""
    pass

# Response schemas
class AfterSaleList(BaseModel):
    """售后列表响应 schema"""
    total: int
    items: List[AfterSale]

class AfterSaleLogList(BaseModel):
    """售后日志列表响应 schema"""
    total: int
    items: List[AfterSaleLog] 