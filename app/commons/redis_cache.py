import redis.asyncio as redis
from ..config import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_USERNAME = settings.REDIS_USERNAME
REDIS_PASSWORD = settings.REDIS_PASSWORD


class RedisCache:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.decode_responses = True

    async def connect(self):
        self.client = await redis.Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            decode_responses=self.decode_responses,
        )

    async def disconnect(self):
        await self.client.aclose()


cache = RedisCache(REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD)
