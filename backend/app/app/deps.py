import redis.asyncio
from fastapi import Depends

from app.config import settings
from app.utils.cache import Cache


async def get_redis():
    """Создаем соединение с базой Redis"""
    return redis.asyncio.Redis.from_url(
        settings.REDIS_URL,
    )


async def get_cache(redis_instance=Depends(get_redis)):
    """Создаем объект кэша"""
    return Cache(redis=redis_instance, ttl=settings.CACHE_TTL)
