from typing import Any, Dict, List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.product import Product, Category, ProductImage, ProductSKU
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    CategoryCreate,
    CategoryUpdate,
    ProductImageCreate,
    ProductImageUpdate,
    ProductSKUCreate,
    ProductSKUUpdate,
)


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Product]:
        """
        根据商品名称获取商品
        """
        result = await db.execute(select(Product).filter(Product.name == name))
        return result.scalar_one_or_none()

    async def get_multi_by_category(
        self, db: AsyncSession, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        获取指定分类下的商品列表
        """
        result = await db.execute(
            select(Product)
            .filter(Product.category_id == category_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        """
        根据分类名称获取分类
        """
        result = await db.execute(select(Category).filter(Category.name == name))
        return result.scalar_one_or_none()


class CRUDProductImage(CRUDBase[ProductImage, ProductImageCreate, ProductImageUpdate]):
    async def get_by_product(
        self, db: AsyncSession, *, product_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProductImage]:
        """
        获取指定商品的图片列表
        """
        result = await db.execute(
            select(ProductImage)
            .filter(ProductImage.product_id == product_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDProductSKU(CRUDBase[ProductSKU, ProductSKUCreate, ProductSKUUpdate]):
    async def get_by_product(
        self, db: AsyncSession, *, product_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProductSKU]:
        """
        获取指定商品的SKU列表
        """
        result = await db.execute(
            select(ProductSKU)
            .filter(ProductSKU.product_id == product_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_code(self, db: AsyncSession, *, code: str) -> Optional[ProductSKU]:
        """
        根据SKU编码获取SKU
        """
        result = await db.execute(select(ProductSKU).filter(ProductSKU.code == code))
        return result.scalar_one_or_none()


product = CRUDProduct(Product)
category = CRUDCategory(Category)
product_image = CRUDProductImage(ProductImage)
product_sku = CRUDProductSKU(ProductSKU) 