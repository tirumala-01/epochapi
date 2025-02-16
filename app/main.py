from fastapi import FastAPI
from .routers import router as api_router
from contextlib import asynccontextmanager
from .commons.postgres import database
from .commons.redis_cache import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    await database.connect()
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
