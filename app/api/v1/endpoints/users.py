from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.api import deps
from app.services.user import user_service

router = APIRouter()


@router.get("/", response_model=List[schemas.UserInDB])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    获取用户列表
    """
    users = await user_service.get_users(db=db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.UserInDB)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建新用户
    """
    user = await user_service.get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await user_service.create_user(db=db, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.UserInDB)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取当前用户信息
    """
    return current_user


@router.put("/me", response_model=schemas.UserInDB)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新当前用户信息
    """
    user = await user_service.update_user(
        db=db, user_id=current_user.id, obj_in=user_in
    )
    return user


@router.get("/{user_id}", response_model=schemas.UserInDB)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    通过ID获取用户信息
    """
    user = await user_service.get_user(db=db, user_id=user_id)
    if user == current_user:
        return user
    if not await user_service.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.UserInDB)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    更新用户信息
    """
    user = await user_service.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await user_service.update_user(
        db=db, user_id=user_id, obj_in=user_in
    )
    return user 