import arq
from arq.connections import RedisSettings


redis_settings = RedisSettings.from_dsn("redis://localhost:6379")
redis_pool = None


async def create_redis_pool():
    """Creates an ARQ Redis connection pool."""
    global redis_pool
    redis_pool = await arq.create_pool(redis_settings)


async def close_redis_pool():
    """Closes the ARQ Redis connection pool."""
    if redis_pool:
        await redis_pool.close()


async def get_redis_pool() -> arq.ArqRedis:
    """FastAPI dependency to get the Redis pool."""
    return redis_pool
