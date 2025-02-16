from typing import List
from fastapi import APIRouter
from loguru import logger
from app.crud.shipment import origin_cities, destination_cities

router = APIRouter(prefix="/city")


@router.get("/origin")
async def get_origin_cities()->List[str]:
    origins = await origin_cities()
    return origins


@router.get("/destination")
async def get_destination_cities()->List[str]:
    destinations = await destination_cities()
    return destinations