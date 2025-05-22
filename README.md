# Mall Admin API

商城管理系统后端API

## 功能特性

- 用户认证和授权
- 用户管理
- 商品管理
- 订单管理
- 售后管理
- 数据统计

## 技术栈

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- JWT

## 开发环境设置

1. 克隆项目

```bash
git clone https://github.com/yourusername/mall-admin-api.git
cd mall-admin-api
```

2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

5. 初始化数据库

```bash
alembic upgrade head
```

6. 运行开发服务器

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 4010
```

7. 运行Celery Worker

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

8. 运行Celery Beat

```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

## Docker部署

1. 构建镜像

```bash
docker build -t mall-admin-api .
```

2. 运行容器

```bash
# 运行API服务
docker run -d --name mall-admin-api -p 4010:4010 mall-admin-api api

# 运行Celery Worker
docker run -d --name mall-admin-celery-worker mall-admin-api celery worker

# 运行Celery Beat
docker run -d --name mall-admin-celery-beat mall-admin-api celery beat
```

## API文档

启动服务后访问以下地址查看API文档：

- Swagger UI: http://localhost:4010/docs
- ReDoc: http://localhost:4010/redoc

## 定时任务

系统包含以下定时任务：

1. 每日统计数据生成
   - 任务：`app.tasks.statistics.generate_daily_statistics`
   - 频率：每天执行一次
   - 功能：生成前一天的销售趋势和商品排行数据

## 测试

运行测试：

```bash
pytest
```

## 许可证

MIT 