from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# OrderItem schemas
class OrderItemBase(BaseModel):
    product_id: int
    sku_id: int
    quantity: int = Field(..., gt=0)
    price: float
    total_price: float
    extra: Optional[Dict[str, Any]] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = None
    total_price: Optional[float] = None
    extra: Optional[Dict[str, Any]] = None

class OrderItemInDB(OrderItemBase):
    id: int
    order_id: int
    product_name: str
    product_image: Optional[str]
    sku_code: Optional[str]
    sku_attributes: Optional[dict]
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderItem(OrderItemInDB):
    pass

# Order schemas
class OrderBase(BaseModel):
    receiver_name: str
    receiver_phone: str
    receiver_province: str
    receiver_city: str
    receiver_district: str
    receiver_address: str
    remark: Optional[str] = None
    user_id: int
    order_no: str
    total_amount: float
    status: str
    payment_method: Optional[str] = None
    payment_time: Optional[datetime] = None
    shipping_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    cancel_time: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_method: Optional[str] = None
    payment_time: Optional[datetime] = None
    shipping_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    cancel_time: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    remark: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class OrderInDB(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemInDB]

    class Config:
        from_attributes = True

class Order(OrderInDB):
    pass

# OrderLog schemas
class OrderLogBase(BaseModel):
    action: str
    operator: str
    remark: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class OrderLogCreate(OrderLogBase):
    order_id: int

class OrderLogUpdate(BaseModel):
    action: Optional[str] = None
    operator: Optional[str] = None
    remark: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

class OrderLogInDB(OrderLogBase):
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderLog(OrderLogInDB):
    pass

# Response schemas
class OrderList(BaseModel):
    total: int
    items: List[Order]

class OrderItemList(BaseModel):
    total: int
    items: List[OrderItem]

class OrderLogList(BaseModel):
    total: int
    items: List[OrderLog] 