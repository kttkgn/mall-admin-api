from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    async def get_user(
        db: AsyncSession,
        *,
        user_id: int
    ) -> Optional[models.User]:
        """
        获取用户详情
        """
        return await crud.user.get(db=db, id=user_id)

    @staticmethod
    async def get_user_by_email(
        db: AsyncSession,
        *,
        email: str
    ) -> Optional[models.User]:
        """
        通过邮箱获取用户
        """
        return await crud.user.get_by_email(db=db, email=email)

    @staticmethod
    async def get_users(
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.User]:
        """
        获取用户列表
        """
        return await crud.user.get_multi(db=db, skip=skip, limit=limit)

    @staticmethod
    async def create_user(
        db: AsyncSession,
        *,
        obj_in: UserCreate
    ) -> models.User:
        """
        创建用户
        """
        user_data = obj_in.dict()
        user_data["hashed_password"] = get_password_hash(obj_in.password)
        del user_data["password"]
        return await crud.user.create(db=db, obj_in=user_data)

    @staticmethod
    async def update_user(
        db: AsyncSession,
        *,
        user_id: int,
        obj_in: UserUpdate
    ) -> Optional[models.User]:
        """
        更新用户
        """
        user = await crud.user.get(db=db, id=user_id)
        if not user:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]
        return await crud.user.update(db=db, db_obj=user, obj_in=update_data)

    @staticmethod
    async def authenticate(
        db: AsyncSession,
        *,
        email: str,
        password: str
    ) -> Optional[models.User]:
        """
        用户认证
        """
        user = await crud.user.get_by_email(db=db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def is_active(user: models.User) -> bool:
        """
        检查用户是否激活
        """
        return user.is_active

    @staticmethod
    async def is_superuser(user: models.User) -> bool:
        """
        检查用户是否是超级管理员
        """
        return user.is_superuser


user_service = UserService() 