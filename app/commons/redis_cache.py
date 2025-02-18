import redis.asyncio as redis
from ..config import settings

REDIS_HOST = settings.REDIS_HOST

class RedisCache:
    async def connect(self):
        pool = redis.ConnectionPool(
            host=REDIS_HOST,
            decode_responses=True
        )
        self.client = await redis.Redis(connection_pool=pool)

    async def disconnect(self):
        await self.client.aclose()


cache = RedisCache()
