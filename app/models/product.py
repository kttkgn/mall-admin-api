from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin

class Product(Base, TimestampMixin):
    """商品表"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    name = Column(String(100), nullable=False, index=True, comment="商品名称")
    description = Column(Text, comment="商品描述")
    price = Column(Float, nullable=False, comment="商品价格")
    original_price = Column(Float, comment="商品原价")
    stock = Column(Integer, default=0, comment="库存")
    sales = Column(Integer, default=0, comment="销量")
    category_id = Column(Integer, ForeignKey("categories.id"), comment="分类ID")
    status = Column(Enum('draft', 'on_sale', 'off_sale', name='product_status'), default='draft', comment="状态：draft-草稿，on_sale-在售，off_sale-下架")
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    is_recommended = Column(Boolean, default=False, comment="是否热门")
    main_image = Column(String(200), comment="主图")
    is_active = Column(Boolean, default=True, comment="是否启用")
    brand = Column(String(50), comment="品牌")
    unit = Column(String(20), comment="单位")
    weight = Column(Float, comment="重量")
    volume = Column(Float, comment="体积")
    sort_order = Column(Integer, default=0, comment="排序")
    
    # 关联
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    skus = relationship("ProductSKU", back_populates="product", cascade="all, delete-orphan")

class Category(Base, TimestampMixin):
    """商品分类表"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    name = Column(String(50), unique=True, index=True, nullable=False, comment="分类名称")
    description = Column(Text, comment="分类描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序")
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True, comment="父分类ID")
    
    # 关联
    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")

class ProductImage(Base, TimestampMixin):
    """商品图片表"""
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    url = Column(String(255), nullable=False, comment="图片URL")
    sort_order = Column(Integer, default=0, comment="排序")
    is_main = Column(Boolean, default=False, comment="是否主图")
    
    # 关联
    product = relationship("Product", back_populates="images")

class ProductSKU(Base, TimestampMixin):
    """商品SKU表"""
    __tablename__ = "product_skus"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    code = Column(String(50), unique=True, index=True, nullable=False, comment="SKU编码")
    name = Column(String(100), nullable=False, comment="SKU名称")
    price = Column(Float, nullable=False, comment="SKU价格")
    original_price = Column(Float, comment="SKU原价")
    stock = Column(Integer, default=0, comment="SKU库存")
    sales = Column(Integer, default=0, comment="SKU销量")
    attributes = Column(JSON, comment="SKU属性，如颜色、尺寸等")
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    # 关联
    product = relationship("Product", back_populates="skus") 