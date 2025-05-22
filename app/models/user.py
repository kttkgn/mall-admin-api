from sqlalchemy import Column, String, Boolean, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base, TimestampMixin, IDMixin

class User(Base, IDMixin, TimestampMixin):
    """用户表"""
    __tablename__ = "users"
    
    username = Column(String(32), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(128), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(128), nullable=False, comment="加密密码")
    full_name = Column(String(128), comment="姓名")
    avatar = Column(String(200), comment="头像")
    role = Column(String(32), default="user", comment="角色：user-普通用户，admin-管理员")
    status = Column(Boolean, default=True, comment="状态：true-启用，false-禁用")
    last_login = Column(DateTime, comment="最后登录时间")
    last_login_ip = Column(String(50), comment="最后登录IP")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员")
    nickname = Column(String(50), comment="昵称")
    phone = Column(String(20), comment="手机号")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关联
    orders = relationship("Order", back_populates="user")
    after_sales = relationship("AfterSale", back_populates="user") 