from fastapi import FastAPI
from .routers import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .commons.postgres import database
from .commons.redis_cache import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    await database.connect()
    yield
    await cache.disconnect()
    database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
