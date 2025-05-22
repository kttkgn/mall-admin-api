from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "mall_admin",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.statistics"]
)

# 配置Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)

# 配置定时任务
celery_app.conf.beat_schedule = {
    "generate-daily-statistics": {
        "task": "app.tasks.statistics.generate_daily_statistics",
        "schedule": 86400.0,  # 每天执行一次
        "args": (),
    },
} 