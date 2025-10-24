from typing import Optional
from redis.asyncio import Redis

redis: Optional[Redis] = None


# A function that initializes Redis Client
async def init_redis():
    global redis
    if redis is None:
        redis = await Redis(decode_responses=True)

    return redis  # Returning here as well so that we can gracefully close Redis connections at shutdown


# Function to get redis client variable, this is done as each worker will have its own redis connection
async def get_redis() -> Redis:
    if redis is None:
        raise RuntimeError(
            "Redis not initialized. Did you forget to call init_redis()?"
        )
    return redis
