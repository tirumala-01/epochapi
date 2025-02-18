from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from typing import Literal
from pydantic import BaseModel
from app.crud.vehicle import get_fuel_info

router = APIRouter(prefix="/fuel-efficiency")


class FuelEfficiency(BaseModel):
    operation: Literal["average", "maximum", "minimum"]


@router.get("/{vehicle_id}")
async def get_fuel_efficiency(vehicle_id: str, q: FuelEfficiency = Query(...)):
    try:
        return await get_fuel_info(vehicle_id, q.operation)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValueError as e:
        logger.error(f"Value error getting fuel efficiency for {vehicle_id}: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
    except Exception as e:
        logger.error(f"Error getting fuel efficiency for {vehicle_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")