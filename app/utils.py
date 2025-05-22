from datetime import datetime, timedelta
from typing import Any, Union
import os

from jose import jwt
from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 邮件配置
email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=os.path.join(os.path.dirname(os.path.dirname(__file__)), "email-templates"),
)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    创建访问令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    获取密码哈希
    """
    return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    """
    生成密码重置令牌
    """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str:
    """
    验证密码重置令牌
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


async def send_reset_password_email(email_to: EmailStr, email: str, token: str) -> None:
    """
    发送密码重置邮件
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - 密码重置"
    reset_link = f"{settings.SERVER_HOST}/reset-password?token={token}"
    
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=f"""
        <html>
            <body>
                <p>您好，</p>
                <p>您收到这封邮件是因为您（或其他人）请求重置您的密码。</p>
                <p>请点击下面的链接重置您的密码：</p>
                <p><a href="{reset_link}">{reset_link}</a></p>
                <p>如果您没有请求重置密码，请忽略此邮件。</p>
                <p>此链接将在 {settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS} 小时后过期。</p>
                <p>谢谢！</p>
                <p>{project_name} 团队</p>
            </body>
        </html>
        """,
        subtype="html",
    )
    
    fm = FastMail(email_conf)
    await fm.send_message(message) 