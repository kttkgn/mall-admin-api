from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer

@as_declarative()
class Base:
    """
    所有模型的基类
    """
    id: Any
    __name__: str
    
    # 生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class TimestampMixin:
    """为模型添加创建时间和更新时间字段"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

class IDMixin:
    """为模型添加主键ID字段"""
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID") 