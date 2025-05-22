from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models
from app.schemas.product import (
    ProductCreate, ProductUpdate,
    CategoryCreate, CategoryUpdate,
    ProductImageCreate, ProductImageUpdate,
    ProductSKUCreate, ProductSKUUpdate
)


class ProductService:
    @staticmethod
    async def get_product(
        db: AsyncSession,
        *,
        product_id: int
    ) -> Optional[models.Product]:
        """
        获取商品详情
        """
        return await crud.product.get(db=db, id=product_id)

    @staticmethod
    async def get_products(
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None
    ) -> List[models.Product]:
        """
        获取商品列表
        """
        if category_id:
            return await crud.product.get_multi_by_category(
                db=db, category_id=category_id, skip=skip, limit=limit
            )
        return await crud.product.get_multi(db=db, skip=skip, limit=limit)

    @staticmethod
    async def create_product(
        db: AsyncSession,
        *,
        obj_in: ProductCreate
    ) -> models.Product:
        """
        创建商品
        """
        return await crud.product.create(db=db, obj_in=obj_in)

    @staticmethod
    async def update_product(
        db: AsyncSession,
        *,
        product_id: int,
        obj_in: ProductUpdate
    ) -> Optional[models.Product]:
        """
        更新商品
        """
        product = await crud.product.get(db=db, id=product_id)
        if not product:
            return None
        return await crud.product.update(db=db, db_obj=product, obj_in=obj_in)

    @staticmethod
    async def delete_product(
        db: AsyncSession,
        *,
        product_id: int
    ) -> Optional[models.Product]:
        """
        删除商品
        """
        product = await crud.product.get(db=db, id=product_id)
        if not product:
            return None
        return await crud.product.remove(db=db, id=product_id)


class CategoryService:
    @staticmethod
    async def get_category(
        db: AsyncSession,
        *,
        category_id: int
    ) -> Optional[models.Category]:
        """
        获取商品分类详情
        """
        return await crud.category.get(db=db, id=category_id)

    @staticmethod
    async def get_categories(
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Category]:
        """
        获取商品分类列表
        """
        return await crud.category.get_multi(db=db, skip=skip, limit=limit)

    @staticmethod
    async def create_category(
        db: AsyncSession,
        *,
        obj_in: CategoryCreate
    ) -> models.Category:
        """
        创建商品分类
        """
        return await crud.category.create(db=db, obj_in=obj_in)

    @staticmethod
    async def update_category(
        db: AsyncSession,
        *,
        category_id: int,
        obj_in: CategoryUpdate
    ) -> Optional[models.Category]:
        """
        更新商品分类
        """
        category = await crud.category.get(db=db, id=category_id)
        if not category:
            return None
        return await crud.category.update(db=db, db_obj=category, obj_in=obj_in)

    @staticmethod
    async def delete_category(
        db: AsyncSession,
        *,
        category_id: int
    ) -> Optional[models.Category]:
        """
        删除商品分类
        """
        category = await crud.category.get(db=db, id=category_id)
        if not category:
            return None
        return await crud.category.remove(db=db, id=category_id)


class ProductImageService:
    @staticmethod
    async def get_image(
        db: AsyncSession,
        *,
        image_id: int
    ) -> Optional[models.ProductImage]:
        """
        获取商品图片详情
        """
        return await crud.product_image.get(db=db, id=image_id)

    @staticmethod
    async def get_images_by_product(
        db: AsyncSession,
        *,
        product_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.ProductImage]:
        """
        获取商品图片列表
        """
        return await crud.product_image.get_by_product(
            db=db, product_id=product_id, skip=skip, limit=limit
        )

    @staticmethod
    async def create_image(
        db: AsyncSession,
        *,
        obj_in: ProductImageCreate
    ) -> models.ProductImage:
        """
        创建商品图片
        """
        return await crud.product_image.create(db=db, obj_in=obj_in)

    @staticmethod
    async def update_image(
        db: AsyncSession,
        *,
        image_id: int,
        obj_in: ProductImageUpdate
    ) -> Optional[models.ProductImage]:
        """
        更新商品图片
        """
        image = await crud.product_image.get(db=db, id=image_id)
        if not image:
            return None
        return await crud.product_image.update(db=db, db_obj=image, obj_in=obj_in)

    @staticmethod
    async def delete_image(
        db: AsyncSession,
        *,
        image_id: int
    ) -> Optional[models.ProductImage]:
        """
        删除商品图片
        """
        image = await crud.product_image.get(db=db, id=image_id)
        if not image:
            return None
        return await crud.product_image.remove(db=db, id=image_id)


class ProductSKUService:
    @staticmethod
    async def get_sku(
        db: AsyncSession,
        *,
        sku_id: int
    ) -> Optional[models.ProductSKU]:
        """
        获取商品SKU详情
        """
        return await crud.product_sku.get(db=db, id=sku_id)

    @staticmethod
    async def get_skus_by_product(
        db: AsyncSession,
        *,
        product_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.ProductSKU]:
        """
        获取商品SKU列表
        """
        return await crud.product_sku.get_by_product(
            db=db, product_id=product_id, skip=skip, limit=limit
        )

    @staticmethod
    async def create_sku(
        db: AsyncSession,
        *,
        obj_in: ProductSKUCreate
    ) -> models.ProductSKU:
        """
        创建商品SKU
        """
        return await crud.product_sku.create(db=db, obj_in=obj_in)

    @staticmethod
    async def update_sku(
        db: AsyncSession,
        *,
        sku_id: int,
        obj_in: ProductSKUUpdate
    ) -> Optional[models.ProductSKU]:
        """
        更新商品SKU
        """
        sku = await crud.product_sku.get(db=db, id=sku_id)
        if not sku:
            return None
        return await crud.product_sku.update(db=db, db_obj=sku, obj_in=obj_in)

    @staticmethod
    async def delete_sku(
        db: AsyncSession,
        *,
        sku_id: int
    ) -> Optional[models.ProductSKU]:
        """
        删除商品SKU
        """
        sku = await crud.product_sku.get(db=db, id=sku_id)
        if not sku:
            return None
        return await crud.product_sku.remove(db=db, id=sku_id)


product_service = ProductService()
category_service = CategoryService()
product_image_service = ProductImageService()
product_sku_service = ProductSKUService() 