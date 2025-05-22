from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
import logging
from app.core.config import settings

# 配置日志
logger = logging.getLogger(__name__)

# 配置密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    """
    try:
        logger.info(f"开始验证密码 - 明文密码: {plain_password}, 哈希密码: {hashed_password}")
        
        # 检查参数
        if not plain_password or not hashed_password:
            logger.error("密码验证失败 - 密码为空")
            return False
            
        # 验证密码
        result = pwd_context.verify(plain_password, hashed_password)
        logger.info(f"密码验证结果: {result}")
        return result
        
    except Exception as e:
        logger.error(f"密码验证失败 - 错误: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """
    获取密码哈希值
    """
    try:
        logger.info(f"开始生成密码哈希 - 密码: {password}")
        
        # 检查参数
        if not password:
            raise ValueError("密码不能为空")
            
        # 生成哈希
        hashed = pwd_context.hash(password)
        logger.info(f"密码哈希生成成功 - 哈希: {hashed}")
        return hashed
        
    except Exception as e:
        logger.error(f"密码哈希生成失败 - 错误: {str(e)}")
        raise 