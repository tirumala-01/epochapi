from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from typing import List, Literal
from pydantic import BaseModel
from app.crud.shipment import get_total_ship_cost
from app.schemas.shipment import ShipmentCost


router = APIRouter(prefix="/expensive-routes")

class RouteType(BaseModel):
    operation: Literal["highest", "lowest"]

@router.get("")
async def get_expensive_routes(q: RouteType = Query(...)) -> List[ShipmentCost]:
    try:
        logger.info(f"Getting {q.operation} expensive routes")
        if q.operation == "highest":
            result = await get_total_ship_cost(q.operation)
        else:
            result = await get_total_ship_cost(q.operation)
        return result
    except Exception as e:
        logger.error(f"Error getting {e} expensive routes")
        raise HTTPException(status_code=500, detail="Internal Server Error")