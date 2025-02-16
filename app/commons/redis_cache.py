import redis
from ..config import settings

REDIS_HOST = settings.REDIS_HOST

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    redis_client.ping()
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Error connecting to Redis: {e}")
    redis_client = None


def get_redis():
    if redis_client:
        try:
            yield redis_client
        finally:
            pass
    else:
        yield None
