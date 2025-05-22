from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.api import deps
from app.services.order import order_service

router = APIRouter()


@router.get("/", response_model=List[schemas.OrderInDB])
async def read_orders(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取订单列表
    """
    if not crud.user.is_superuser(current_user):
        orders = await order_service.get_orders(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    else:
        orders = await order_service.get_orders(db=db, skip=skip, limit=limit)
    return orders


@router.post("/", response_model=schemas.OrderInDB)
async def create_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_in: schemas.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新订单
    """
    order = await order_service.create_order(
        db=db, obj_in=order_in, user_id=current_user.id
    )
    return order


@router.get("/{order_id}", response_model=schemas.OrderInDB)
async def read_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取订单详情
    """
    order = await order_service.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not crud.user.is_superuser(current_user) and order.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return order


@router.put("/{order_id}", response_model=schemas.OrderInDB)
async def update_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_id: int,
    order_in: schemas.OrderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新订单
    """
    order = await order_service.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not crud.user.is_superuser(current_user) and order.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    order = await order_service.update_order(
        db=db, order_id=order_id, obj_in=order_in
    )
    return order


@router.get("/{order_id}/logs", response_model=List[schemas.OrderLogInDB])
async def read_order_logs(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取订单日志
    """
    order = await order_service.get_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not crud.user.is_superuser(current_user) and order.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    logs = await order_service.get_order_logs(db=db, order_id=order_id)
    return logs 