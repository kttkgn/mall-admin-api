from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 创建连接池
pool = ConnectionPool.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
    socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
    retry_on_timeout=True,
)

# 创建 Redis 客户端
redis = Redis(connection_pool=pool)

async def get_redis() -> Redis:
    """
    获取 Redis 连接
    """
    try:
        await redis.ping()
        return redis
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")
        raise

async def close_redis():
    """
    关闭 Redis 连接
    """
    try:
        await redis.close()
        await pool.disconnect()
    except Exception as e:
        logger.error(f"Redis close error: {str(e)}")
        raise 