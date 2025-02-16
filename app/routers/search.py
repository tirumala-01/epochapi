from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix="/search")


@router.get("")
async def get_shipment_information(query: str):
    logger.info(f"Searching for {query}")

    return {
        "query": query,
    }
