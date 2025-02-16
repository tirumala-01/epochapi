from fastapi import APIRouter, Query
from loguru import logger
from typing import Annotated, Literal
from pydantic import BaseModel

router = APIRouter(prefix="/delivery-time")


class DeliveryTime(BaseModel):
    operation: Literal["average", "maximum", "minimum"]


@router.get("/{origin}/{destination}")
async def get_delivery_time(
    origin: str, destination: str, q: Annotated[DeliveryTime, Query()] = "average"
):
    logger.info(f"Calculating {q} delivery time from {origin} to {destination}")
    return {
        "delivery_time": 2,
        "origin": origin,
        "destination": destination,
        "operation": q.operation,
    }
