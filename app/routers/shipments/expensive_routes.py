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
        return await get_total_ship_cost(q.operation)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValueError as e:
        logger.error(f"Value error getting expensive routes: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
    except Exception as e:
        logger.error(f"Error getting {e} expensive routes")
        raise HTTPException(status_code=500, detail="Internal Server Error")