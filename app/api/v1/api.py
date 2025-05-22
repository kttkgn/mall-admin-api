from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, products, orders, after_sales, statistics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(after_sales.router, prefix="/after-sales", tags=["after-sales"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"]) 