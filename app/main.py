from fastapi import FastAPI
from .routers import router as api_router
from contextlib import asynccontextmanager
from .commons.postgres import database
from .commons.postgres_helper import setup_prepared_statements
from .commons.redis_cache import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    await database.connect()
    await setup_prepared_statements()
    yield
    await cache.disconnect()
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
