from fastapi import APIRouter
from typing import List
from app.crud.shipment import get_high_ship_cost, get_low_ship_cost
from app.schemas.shipment import HighestShipmentCost, LowestShipmentCost


router = APIRouter(prefix="/total-shipment-cost")


@router.get("/highest")
async def get_high_shipment_costs() -> List[HighestShipmentCost]:
    result = await get_high_ship_cost()
    return result


@router.get("/lowest")
async def get_low_shipment_costs() -> List[LowestShipmentCost]:
    result = await get_low_ship_cost()
    return result
