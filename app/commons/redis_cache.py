import redis.asyncio as redis
from ..config import settings

REDIS_HOST = settings.REDIS_HOST
ENVIRONMENT = settings.ENVIRONMENT

class RedisCache:
    async def connect(self):
        if ENVIRONMENT == "local":
            self.client = await redis.Redis(
                host='localhost',
                decode_responses=True,
                db=0,
            )
        else:
            self.client = await redis.RedisCluster(
                host=REDIS_HOST, decode_responses=True, db=0
            )

    async def disconnect(self):
        await self.client.aclose()


cache = RedisCache()
