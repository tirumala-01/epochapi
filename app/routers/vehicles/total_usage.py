from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix="/total-usage")


@router.get("/{vehicle_id}")
async def get_total_usage(vehicle_id: int):
    logger.info(f"Getting total usage for vehicle {vehicle_id}")
    return {"vehicle_id": "V-001", "fuel_consumed": 100, "distance_travelled": 1000}