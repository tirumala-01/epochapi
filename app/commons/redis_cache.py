import redis.asyncio as redis
from ..config import settings

REDIS_HOST = settings.REDIS_HOST


class RedisCache:
    async def connect(self):
        self.client = await redis.RedisCluster(host=REDIS_HOST, decode_responses=True, db=0)

    async def disconnect(self):
        await self.client.aclose()


cache = RedisCache()
