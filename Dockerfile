FROM python:3.9

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建启动脚本
RUN echo '#!/bin/bash\n\
if [ "$1" = "celery" ]; then\n\
    if [ "$2" = "worker" ]; then\n\
        celery -A app.tasks.celery_app worker --loglevel=info\n\
    elif [ "$2" = "beat" ]; then\n\
        celery -A app.tasks.celery_app beat --loglevel=info\n\
    fi\n\
else\n\
    uvicorn app.main:app --host 0.0.0.0 --port 4010 --reload\n\
fi' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 4010

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["api"] 