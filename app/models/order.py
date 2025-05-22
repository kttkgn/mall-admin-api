from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin
from datetime import datetime


class Order(Base, TimestampMixin):
    """订单表"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    order_no = Column(String(50), unique=True, index=True, nullable=False, comment="订单编号")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    total_amount = Column(Float, nullable=False, comment="订单总金额")
    status = Column(Enum('pending', 'paid', 'shipped', 'completed', 'cancelled', 'refunded', name='order_status'), default='pending', comment="订单状态")
    payment_method = Column(String(50), comment="支付方式")
    payment_time = Column(DateTime, comment="支付时间")
    shipping_time = Column(DateTime, comment="发货时间")
    completion_time = Column(DateTime, comment="完成时间")
    cancel_time = Column(DateTime, comment="取消时间")
    cancel_reason = Column(String(200), comment="取消原因")
    receiver_name = Column(String(50), nullable=False, comment="收货人姓名")
    receiver_phone = Column(String(20), nullable=False, comment="收货人电话")
    receiver_province = Column(String(50), nullable=False, comment="省份")
    receiver_city = Column(String(50), nullable=False, comment="城市")
    receiver_district = Column(String(50), nullable=False, comment="区县")
    receiver_address = Column(String(200), nullable=False, comment="详细地址")
    receiver_zip = Column(String(20), comment="邮政编码")
    remark = Column(Text, comment="订单备注")
    shipping_address = Column(JSON, comment="收货地址")
    shipping_fee = Column(Float, default=0, comment="运费")
    discount_amount = Column(Float, default=0, comment="优惠金额")
    
    # 关联
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    logs = relationship("OrderLog", back_populates="order", cascade="all, delete-orphan")
    after_sales = relationship("AfterSale", back_populates="order")


class OrderItem(Base, TimestampMixin):
    """订单商品表"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, comment="订单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    product_sku_id = Column(Integer, ForeignKey("product_skus.id"), nullable=False, comment="商品SKU ID")
    product_name = Column(String(100), nullable=False, comment="商品名称")
    product_sku_name = Column(String(100), nullable=False, comment="SKU名称")
    product_image = Column(String(200), comment="商品图片")
    quantity = Column(Integer, nullable=False, comment="购买数量")
    price = Column(Float, nullable=False, comment="购买单价")
    total_amount = Column(Float, nullable=False, comment="总金额")
    total_price = Column(Float, nullable=False, comment="总价")
    sku_attributes = Column(JSON, comment="SKU属性")
    
    # 关联
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    product_sku = relationship("ProductSKU")
    after_sales = relationship("AfterSale", back_populates="order_item")


class OrderLog(Base, TimestampMixin):
    """订单日志表"""
    __tablename__ = "order_logs"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, comment="订单ID")
    action = Column(String(50), nullable=False, comment="操作类型")
    operator = Column(String(50), comment="操作人")
    remark = Column(Text, comment="备注")
    extra = Column(JSON, comment="额外信息")
    
    # 关联
    order = relationship("Order", back_populates="logs") 