from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    用户基础模型
    """
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    role: Optional[str] = "user"  # 用户角色：user/admin

class UserCreate(UserBase):
    """
    创建用户模型
    """
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    """
    更新用户模型
    """
    password: Optional[str] = None

class UserInDBBase(UserBase):
    """
    数据库中的用户基础模型
    """
    id: Optional[int] = None

    class Config:
        from_attributes = True

class UserInDB(UserInDBBase):
    """
    数据库中的用户模型
    """
    hashed_password: str

class User(UserInDBBase):
    """
    用户模型
    """
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class UserList(BaseModel):
    """
    用户列表响应模型
    """
    total: int
    items: List[User] 