from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from typing import Literal
from pydantic import BaseModel
from app.crud.shipment import get_ship_cost

router = APIRouter(prefix="/cost")

class RouteCost(BaseModel):
    operation: Literal["average", "maximum", "minimum", "total"]


@router.get("/{origin}/{destination}")
async def get_route_cost(origin: str, destination: str, q: RouteCost = Query(...)):
    try:
        return await get_ship_cost(origin, destination, q.operation)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValueError as e:
        logger.error(f"Value error getting fuel efficiency for {origin}-{destination}: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
    except Exception as e:
        logger.error(f"Error getting shipment costs for {origin}-{destination}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
