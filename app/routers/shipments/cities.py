from typing import List, Literal
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from loguru import logger
from app.crud.shipment import get_city_names

router = APIRouter(prefix="/cities")


class Type(BaseModel):
    type: Literal["origin", "destination"]


@router.get("")
async def get_cities(q: Type = Query(...)) -> List[str]:
    try:
        logger.info(f"Getting {q.type} cities")
        if q.type == "origin":
            result = await get_city_names(q.type)
        else:
            result = await get_city_names(q.type)
        return result
    except Exception as e:
        logger.error(f"Error getting {e} cities")
        raise HTTPException(status_code=500, detail="Internal Server Error")
