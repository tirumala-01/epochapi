from fastapi import APIRouter, HTTPException
from loguru import logger
from app.crud.vehicle import get_usage_info

router = APIRouter(prefix="/total-usage")


@router.get("/{vehicle_id}")
async def get_total_usage(vehicle_id: str):
    try:
        return await get_usage_info(vehicle_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValueError as e:
        logger.error(f"Value error getting total usage for {vehicle_id}: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
    except Exception as e:
        logger.error(f"Error getting total usage for {vehicle_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")