from loguru import logger
from .redis_cache import cache


async def register_lua_script(script):
    try:
        sha = await cache.client.script_load(script)
        return sha
    except Exception as e:
        logger.debug(f"Error loading Lua script: {e}")


async def hset(name, key, value):
    try:
        await cache.client.hset(name, key, value)
        # await cache.client.expire(key, 604800)
    except Exception as e:
        logger.debug(f"Error setting hash value: {e}")


async def hget(name, key):
    try:
        result = await cache.client.hget(name, key)
        return result
    except Exception as e:
        logger.debug(f"Error getting hash value: {e}")


async def hgetall(name):
    try:
        result = await cache.client.hgetall(name)
        return result
    except Exception as e:
        logger.debug(f"Error getting all hash values: {e}")


async def rpush(key, list):
    try:
        await cache.client.rpush(key, *list)
        # await cache.client.expire(key, 604800)
    except Exception as e:
        logger.debug(f"Error settign list: {e}")


async def lrangeall(key):
    try:
        result = await cache.client.lrange(key, 0, -1)
        return result
    except Exception as e:
        logger.debug(f"Error getting all list values: {e}")


async def set(key, value):
    try:
        await cache.client.set(key, value)
        # await cache.client.expire(key, 604800)
    except Exception as e:
        logger.debug(f"Error setting value: {e}")


async def get(key):
    try:
        result = await cache.client.get(key)
        return result
    except Exception as e:
        logger.debug(f"Error getting value: {e}")