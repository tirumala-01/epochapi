import redis.asyncio as redis
from ..config import settings

REDIS_HOST = settings.REDIS_HOST

class RedisCache:
    def __init__(self, host):
        self.host = host
        self.decode_responses = True

    async def connect(self):
        self.client = await redis.Redis(host=self.host,decode_responses=self.decode_responses)

    async def disconnect(self):
        await self.client.aclose()


cache = RedisCache(REDIS_HOST)
