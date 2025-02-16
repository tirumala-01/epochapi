import re
from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from typing import Annotated, Literal
from pydantic import BaseModel
from app.schemas.shipment import CostByRoute
from app.crud.shipment import get_ship_cost

router = APIRouter(prefix="/cost")

ciyRe = "^(?=[a-zA-Z])[a-zA-Z ]+$"


class RouteCost(BaseModel):
    operation: Literal["average", "maximum", "minimum", "total"]


@router.get("/{origin}/{destination}")
async def get_route_cost(origin: str, destination: str, q: RouteCost = Query(...)):
    try:
        if not (re.match(ciyRe, origin) and re.match(ciyRe, destination)):
            logger.error(f"Invalid origin or destination {origin}-{destination}")
            raise HTTPException(status_code=400, detail="Invalid origin or destination")

        logger.info(f"Getting {q.operation} shipment costs for {origin}-{destination}")
        print(f"{origin}, {destination}")
        if q.operation == "average":
            return
        elif q.operation == "maximum":
            return
        elif q.operation == "minimum":
            return
        elif q.operation == "total":
            return

    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error getting shipment costs for {origin}-{destination}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
