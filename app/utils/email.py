import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_email(
    email_to: str,
    subject: str,
    html: str,
) -> None:
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_TLS
    msg["To"] = email_to
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)

def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    subject = "密码重置"
    html = f"""
    <p>您好，</p>
    <p>请点击下面的链接重置密码：</p>
    <p><a href="{settings.SERVER_HOST}/reset-password?token={token}">重置密码</a></p>
    <p>如果您没有请求重置密码，请忽略此邮件。</p>
    """
    send_email(email_to=email_to, subject=subject, html=html) 