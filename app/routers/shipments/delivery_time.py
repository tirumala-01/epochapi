from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from typing import Literal
from pydantic import BaseModel
from app.crud.shipment import get_ship_time

router = APIRouter(prefix="/delivery-time")


class DeliveryTime(BaseModel):
    operation: Literal["average", "maximum", "minimum", "total"]


@router.get("/{origin}/{destination}")
async def get_delivery_time(
    origin: str, destination: str, q: DeliveryTime = Query(...)
):
    try:
        return await get_ship_time(origin, destination, q.operation)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValueError as e:
        logger.error(f"Value error getting fuel efficiency for for {origin}-{destination}: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
    except Exception as e:
        logger.error(f"Error getting shipment times for {origin}-{destination}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
