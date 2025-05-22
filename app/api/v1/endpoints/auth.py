from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils import (
    generate_password_reset_token,
    verify_password_reset_token,
    send_reset_password_email,
)

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    db: Session = Depends(deps.get_db),
    login_data: LoginRequest = Body(...)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info(f"开始处理登录请求 - 用户名: {login_data.username}")
    
    try:
        # 验证用户
        user = await crud.user.authenticate(
            db, username=login_data.username, password=login_data.password
        )
        
        if not user:
            logger.warning(f"登录失败 - 用户名或密码错误: {login_data.username}")
            raise HTTPException(status_code=400, detail="用户名或密码错误")
            
        if not user.status:
            logger.warning(f"登录失败 - 用户已被禁用: {login_data.username}")
            raise HTTPException(status_code=400, detail="用户已被禁用")
            
        # 生成访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
        
        logger.info(f"登录成功 - 用户: {login_data.username}, 角色: {user.role}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
        
    except Exception as e:
        logger.error(f"登录过程发生错误 - 用户名: {login_data.username}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail="登录过程发生错误")

@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user

@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="该邮箱未注册",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "密码重置邮件已发送"}

@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="无效的token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    elif not user.status:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "密码重置成功"} 