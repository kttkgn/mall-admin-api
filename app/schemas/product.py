from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Category(CategoryInDB):
    pass

# ProductImage schemas
class ProductImageBase(BaseModel):
    url: str
    sort_order: int = 0
    is_main: bool = False

class ProductImageCreate(ProductImageBase):
    product_id: int

class ProductImageUpdate(ProductImageBase):
    url: Optional[str] = None

class ProductImageInDB(ProductImageBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductImage(ProductImageInDB):
    pass

# ProductSKU schemas
class ProductSKUBase(BaseModel):
    code: str
    name: str
    price: float
    stock: int = 0
    attributes: dict
    is_active: bool = True

class ProductSKUCreate(ProductSKUBase):
    product_id: int

class ProductSKUUpdate(ProductSKUBase):
    code: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    attributes: Optional[dict] = None

class ProductSKUInDB(ProductSKUBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductSKU(ProductSKUInDB):
    pass

# Product schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    is_active: bool = True
    category_id: int
    brand: Optional[str] = None
    unit: Optional[str] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    sort_order: int = 0

class ProductCreate(ProductBase):
    images: Optional[List[ProductImageCreate]] = None
    skus: Optional[List[ProductSKUCreate]] = None

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class ProductInDB(ProductBase):
    id: int
    sales: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Product(ProductInDB):
    images: List[ProductImage] = []
    skus: List[ProductSKU] = []

# List schemas
class CategoryList(BaseModel):
    total: int
    items: List[Category]

class ProductList(BaseModel):
    total: int
    items: List[Product]

class ProductImageList(BaseModel):
    total: int
    items: List[ProductImage]

class ProductSKUList(BaseModel):
    total: int
    items: List[ProductSKU] 