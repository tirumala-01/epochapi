from enum import Enum
from fastapi import APIRouter, Query
from loguru import logger
from pydantic import BaseModel

router = APIRouter(prefix="/fuel-efficiency")


class FuelEfficiency(Enum):
    """Category of Fuel Efficiency"""

    AVERAGE = "average"
    MAXIMUM = "maximum"
    MINIMUM = "minimum"


@router.get("/{vehicle_id}")
async def get_fuel_efficiency(
    vehicle_id: str,
    q: FuelEfficiency | None = Query(
        FuelEfficiency.AVERAGE, description="Type of fuel efficiency to get"
    )
):
    logger.info(f"Getting {q} fuel efficiency for vehicle {vehicle_id}")



    return {
        "vehicle_id": vehicle_id,
        "vehicle_full_id": "V-020",
        "vehicle_name": "Vehicle 20",
        "mileage_per_liter": 15.5,
        "operation": q.value,
    }



def getResourceId(xid: str) -> int:
    return int(xid.split("-")[1])