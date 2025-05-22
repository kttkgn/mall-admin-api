from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin

class AfterSale(Base, TimestampMixin):
    """售后表"""
    __tablename__ = "after_sales"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, comment="订单ID")
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False, comment="订单商品ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    type = Column(Enum('refund', 'return', 'exchange', name='after_sale_type'), nullable=False, comment="售后类型：refund-退款，return-退货，exchange-换货")
    reason = Column(String(200), nullable=False, comment="售后原因")
    description = Column(Text, comment="售后描述")
    status = Column(Enum('pending', 'approved', 'rejected', 'processing', 'completed', 'cancelled', name='after_sale_status'), default='pending', comment="售后状态")
    refund_amount = Column(Float, comment="退款金额")
    refund_time = Column(DateTime, comment="退款时间")
    reject_reason = Column(String(200), comment="拒绝原因")
    reject_time = Column(DateTime, comment="拒绝时间")
    complete_time = Column(DateTime, comment="完成时间")
    cancel_time = Column(DateTime, comment="取消时间")
    cancel_reason = Column(String(200), comment="取消原因")
    
    # 退货信息
    return_tracking_no = Column(String(50), comment="退货物流单号")
    return_company = Column(String(50), comment="退货物流公司")
    return_time = Column(DateTime, comment="退货时间")
    
    # 换货信息
    exchange_tracking_no = Column(String(50), comment="换货物流单号")
    exchange_company = Column(String(50), comment="换货物流公司")
    exchange_time = Column(DateTime, comment="换货时间")
    
    # 关联
    order = relationship("Order", back_populates="after_sales")
    order_item = relationship("OrderItem", back_populates="after_sales")
    user = relationship("User", back_populates="after_sales")
    logs = relationship("AfterSaleLog", back_populates="after_sale", cascade="all, delete-orphan")
    items = relationship("AfterSaleItem", back_populates="after_sale", cascade="all, delete-orphan")

class AfterSaleItem(Base, TimestampMixin):
    """售后商品表"""
    __tablename__ = "after_sale_items"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    after_sale_id = Column(Integer, ForeignKey("after_sales.id"), nullable=False, comment="售后单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    product_sku_id = Column(Integer, ForeignKey("product_skus.id"), nullable=False, comment="商品SKU ID")
    quantity = Column(Integer, nullable=False, comment="数量")
    price = Column(Float, nullable=False, comment="单价")
    refund_amount = Column(Float, comment="退款金额")
    reason = Column(String(200), comment="原因")
    
    # 关联
    after_sale = relationship("AfterSale", back_populates="items")
    product = relationship("Product")
    product_sku = relationship("ProductSKU")

class AfterSaleLog(Base, TimestampMixin):
    """售后日志表"""
    __tablename__ = "after_sale_logs"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    after_sale_id = Column(Integer, ForeignKey("after_sales.id"), nullable=False, comment="售后单ID")
    action = Column(String(50), nullable=False, comment="操作类型：申请、审核、退款等")
    operator = Column(String(50), nullable=False, comment="操作人")
    remark = Column(String(200), comment="备注")
    extra = Column(JSON, comment="额外信息")
    
    # 关联
    after_sale = relationship("AfterSale", back_populates="logs") 