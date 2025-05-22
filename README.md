# 商城管理系统后端 API

## 项目说明
这是一个基于 FastAPI 开发的商城管理系统后端 API，提供用户认证、商品管理、订单管理等功能。

## 环境要求
- Python 3.8+
- MySQL 8.0+
- Redis 6.0+

## 安装步骤

1. 克隆项目
```bash
git clone <项目地址>
cd mall-admin-api
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
复制 `.env.example` 文件为 `.env`，并根据实际情况修改配置：
```bash
cp .env.example .env
```

主要配置项说明：
- `DATABASE_URL`: MySQL 数据库连接 URL
- `REDIS_URL`: Redis 连接 URL
- `SECRET_KEY`: JWT 密钥
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token 过期时间（分钟）

5. 初始化数据库
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE mall_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 执行数据库迁移
alembic upgrade head

# 创建管理员用户
mysql -u root -p mall_admin < init_admin.sql
```

## 运行项目

1. 启动开发服务器
```bash
uvicorn app.main:app --reload --port 4010
```

2. 访问 API 文档
- Swagger UI: http://localhost:4010/docs
- ReDoc: http://localhost:4010/redoc

## 默认管理员账号
- 用户名：admin
- 密码：admin123

## API 接口说明

### 认证相关
- POST `/api/v1/auth/login`: 用户登录
- POST `/api/v1/auth/logout`: 用户登出
- GET `/api/v1/auth/me`: 获取当前用户信息

### 用户管理
- GET `/api/v1/users`: 获取用户列表
- POST `/api/v1/users`: 创建用户
- GET `/api/v1/users/{user_id}`: 获取用户详情
- PUT `/api/v1/users/{user_id}`: 更新用户信息
- DELETE `/api/v1/users/{user_id}`: 删除用户

### 商品管理
- GET `/api/v1/products`: 获取商品列表
- POST `/api/v1/products`: 创建商品
- GET `/api/v1/products/{product_id}`: 获取商品详情
- PUT `/api/v1/products/{product_id}`: 更新商品信息
- DELETE `/api/v1/products/{product_id}`: 删除商品

### 订单管理
- GET `/api/v1/orders`: 获取订单列表
- POST `/api/v1/orders`: 创建订单
- GET `/api/v1/orders/{order_id}`: 获取订单详情
- PUT `/api/v1/orders/{order_id}`: 更新订单状态
- DELETE `/api/v1/orders/{order_id}`: 删除订单

## 开发说明

### 项目结构
```
mall-admin-api/
├── alembic/              # 数据库迁移文件
├── app/
│   ├── api/             # API 路由
│   ├── core/            # 核心配置
│   ├── crud/            # 数据库操作
│   ├── db/              # 数据库配置
│   ├── models/          # 数据模型
│   └── schemas/         # 数据验证
├── tests/               # 测试文件
├── .env                 # 环境变量
├── .env.example         # 环境变量示例
├── alembic.ini          # Alembic 配置
├── main.py             # 应用入口
└── requirements.txt     # 项目依赖
```

### 开发规范
1. 遵循 PEP 8 编码规范
2. 使用 Black 进行代码格式化
3. 使用 isort 进行导入排序
4. 使用 flake8 进行代码检查

### 测试
```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app tests/
```

## 部署说明

### 使用 Docker 部署
1. 构建镜像
```bash
docker build -t mall-admin-api .
```

2. 运行容器
```bash
docker run -d -p 4010:4010 --name mall-admin-api mall-admin-api
```

### 使用 Docker Compose 部署
```bash
docker-compose up -d
```

## 常见问题

1. 数据库连接失败
- 检查数据库服务是否启动
- 检查数据库连接配置是否正确
- 检查数据库用户权限

2. Redis 连接失败
- 检查 Redis 服务是否启动
- 检查 Redis 连接配置是否正确

3. Token 验证失败
- 检查 SECRET_KEY 配置是否正确
- 检查 Token 是否过期
- 检查 Token 格式是否正确

## 更新日志

### v1.0.0 (2024-03-20)
- 初始版本发布
- 实现用户认证功能
- 实现商品管理功能
- 实现订单管理功能

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License 