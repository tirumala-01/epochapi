from fastapi import FastAPI
from loguru import logger

import redis

pool = redis.ConnectionPool(host='epoch-app-elasticache.a8tmon.clustercfg.use1.cache.amazonaws.com', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

app = FastAPI()


@app.get("/")
async def root():
    r.set('key', 'value')
    value = r.get('key')
    logger.debug(f"Value: {value}")
    logger.debug("Hello World")
    return {"message": "Hello World"}