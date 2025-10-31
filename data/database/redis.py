from os import getenv

from redis.asyncio import Redis as AsyncRedis

_redis: AsyncRedis | None = None


async def init_redis() -> AsyncRedis:
    global _redis
    if _redis is None:
        url: str = getenv("REDIS_URI", "redis://localhost:6379/0")
        _redis = AsyncRedis.from_url(url, decode_responses=True)
    return _redis


async def get_redis() -> AsyncRedis:
    if _redis is None:
        raise RuntimeError(
            "Redis client not initialized. Did you forget to call init_redis()?"
        )
    return _redis


async def close_redis():
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
