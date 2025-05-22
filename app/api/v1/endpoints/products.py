from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.api import deps
from app.services.product import (
    product_service,
    category_service,
    product_image_service,
    product_sku_service
)

router = APIRouter()

# Category endpoints
@router.get("/categories/", response_model=List[schemas.CategoryInDB])
async def read_categories(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品分类列表
    """
    categories = await category_service.get_categories(
        db=db, skip=skip, limit=limit
    )
    return categories

@router.post("/categories/", response_model=schemas.CategoryInDB)
async def create_category(
    *,
    db: AsyncSession = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建商品分类
    """
    category = await category_service.create_category(
        db=db, obj_in=category_in
    )
    return category

@router.get("/categories/{category_id}", response_model=schemas.CategoryInDB)
async def read_category(
    *,
    db: AsyncSession = Depends(deps.get_db),
    category_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品分类详情
    """
    category = await category_service.get_category(
        db=db, category_id=category_id
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=schemas.CategoryInDB)
async def update_category(
    *,
    db: AsyncSession = Depends(deps.get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    更新商品分类
    """
    category = await category_service.update_category(
        db=db, category_id=category_id, obj_in=category_in
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}", response_model=schemas.CategoryInDB)
async def delete_category(
    *,
    db: AsyncSession = Depends(deps.get_db),
    category_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除商品分类
    """
    category = await category_service.delete_category(
        db=db, category_id=category_id
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Product endpoints
@router.get("/", response_model=List[schemas.ProductInDB])
async def read_products(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品列表
    """
    products = await product_service.get_products(
        db=db, skip=skip, limit=limit, category_id=category_id
    )
    return products

@router.post("/", response_model=schemas.ProductInDB)
async def create_product(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建新商品
    """
    product = await product_service.create_product(db=db, obj_in=product_in)
    return product

@router.get("/{product_id}", response_model=schemas.ProductInDB)
async def read_product(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品详情
    """
    product = await product_service.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.ProductInDB)
async def update_product(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_id: int,
    product_in: schemas.ProductUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    更新商品
    """
    product = await product_service.update_product(
        db=db, product_id=product_id, obj_in=product_in
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=schemas.ProductInDB)
async def delete_product(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除商品
    """
    product = await product_service.delete_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ProductImage endpoints
@router.get("/{product_id}/images/", response_model=List[schemas.ProductImageInDB])
async def read_product_images(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品图片列表
    """
    images = await product_image_service.get_images_by_product(
        db=db, product_id=product_id, skip=skip, limit=limit
    )
    return images

@router.post("/{product_id}/images/", response_model=schemas.ProductImageInDB)
async def create_product_image(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_id: int,
    image_in: schemas.ProductImageCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建商品图片
    """
    image = await product_image_service.create_image(db=db, obj_in=image_in)
    return image

@router.delete("/images/{image_id}", response_model=schemas.ProductImageInDB)
async def delete_product_image(
    *,
    db: AsyncSession = Depends(deps.get_db),
    image_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除商品图片
    """
    image = await product_image_service.delete_image(db=db, image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

# ProductSku endpoints
@router.get("/{product_id}/skus/", response_model=List[schemas.ProductSKUInDB])
async def read_product_skus(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品SKU列表
    """
    skus = await product_sku_service.get_skus_by_product(
        db=db, product_id=product_id, skip=skip, limit=limit
    )
    return skus

@router.post("/{product_id}/skus/", response_model=schemas.ProductSKUInDB)
async def create_product_sku(
    *,
    db: AsyncSession = Depends(deps.get_db),
    product_id: int,
    sku_in: schemas.ProductSKUCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建商品SKU
    """
    sku = await product_sku_service.create_sku(db=db, obj_in=sku_in)
    return sku

@router.put("/skus/{sku_id}", response_model=schemas.ProductSKUInDB)
async def update_product_sku(
    *,
    db: AsyncSession = Depends(deps.get_db),
    sku_id: int,
    sku_in: schemas.ProductSKUUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    更新商品SKU
    """
    sku = await product_sku_service.update_sku(
        db=db, sku_id=sku_id, obj_in=sku_in
    )
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    return sku

@router.delete("/skus/{sku_id}", response_model=schemas.ProductSKUInDB)
async def delete_product_sku(
    *,
    db: AsyncSession = Depends(deps.get_db),
    sku_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除商品SKU
    """
    sku = await product_sku_service.delete_sku(db=db, sku_id=sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    return sku 