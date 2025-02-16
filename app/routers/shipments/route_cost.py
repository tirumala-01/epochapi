from fastapi import APIRouter, Query
from loguru import logger
from typing import Annotated, Literal
from pydantic import BaseModel

router = APIRouter(prefix="/cost")


class RouteCost(BaseModel):
    operation: Literal["average", "maximum", "minimum", "total"]


@router.get("/{origin}/{destination}")
async def get_route_cost(
    origin: str, destination: str, q: Annotated[RouteCost, Query()] = "total"
):
    logger.info(f"Calculating {q} route cost from {origin} to {destination}")
    return {
        "route_cost": 2,
        "origin": origin,
        "destination": destination,
        "operation": q.operation,
    }
