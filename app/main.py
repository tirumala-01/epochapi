from fastapi import FastAPI
from loguru import logger

app = FastAPI()


@app.get("/")
async def root():
    logger.debug("Hello World")
    return {"message": "Hello World"}