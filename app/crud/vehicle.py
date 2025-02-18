import re
import decimal
import asyncpg
from fastapi import HTTPException
from loguru import logger
from app.commons.redis_helper import hgetall, hset
from typing import Any
from app.commons.postgres import database as db
from .util import (
    convert_numbers_to_string,
    get_extracted_id,
    convert_numbers_to_string,
    validate_vehicle_name,
    extract_efficiency_type
)


async def get_fuel_info(vehicle_id: str, operation: str):
    validate_vehicle_name(vehicle_id)
    logger.info(f"Getting {operation} fuel efficiency for {vehicle_id}")

    vehicle_id = get_extracted_id(vehicle_id)
    cache_key = f"vhmileage:{vehicle_id}:details"
    result = await hgetall(cache_key)

    if result:
        logger.debug(f"{cache_key} cache hit")
        return extract_efficiency_type(result, operation)

    results = await db.get_vehicle_efficiency(vehicle_id)
    if results:
        result = convert_numbers_to_string(dict(results))
        await hset(cache_key, result)
        return extract_efficiency_type(result, operation)
    else:
        return {"fuel efficiency": "notfound"}


async def get_usage_info(vehicle_id: str):
    validate_vehicle_name(vehicle_id)
    logger.info(f"Getting usage info for {vehicle_id}")

    vehicle_id = get_extracted_id(vehicle_id)
    cache_key = f"fuelmileage:{vehicle_id}:details"
    result = await hgetall(cache_key)

    if result:
        logger.debug(f"{cache_key} cache hit")
        return result

    results = await db.get_vehicle_fuelmileage(vehicle_id)
    if results:
        results = convert_numbers_to_string(dict(results))
        await hset(cache_key, results)
        return results
    else:
        return {"usage info": "notfound"}
