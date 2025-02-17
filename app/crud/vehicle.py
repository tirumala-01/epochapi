import re
import decimal
import asyncpg
from fastapi import HTTPException
from loguru import logger
from app.commons.redis_helper import hgetall, hset
from typing import Dict, Any
from app.commons.postgres import database


def validate_vehicle_name(vehicle_id):
    vehicle_id_re = "^V-(0{2}[1-9]|[1-9][0-9]{2})$"
    if not re.match(vehicle_id_re, vehicle_id):
        logger.error(f"Invalid Vehicle Id {vehicle_id}")
        raise ValueError("Invalid Vehicle Id")


def extract_efficiency_type(data: Dict[str, Any], metric: str) -> Dict[str, Any]:
    valid_metrics = {
        "average": "avg_mileage_per_liter",
        "maximum": "max_mileage_per_liter",
        "minimum": "min_mileage_per_liter",
    }
    metric_key = valid_metrics[metric]
    filtered_entry = {
        key: value
        for key, value in data.items()
        if key
        in {"vehicle_id", "vehicle_full_id", "vehicle_name", "total_trips", metric_key}
    }
    return filtered_entry


def convert_numbers_to_string(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: convert_numbers_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numbers_to_string(item) for item in data]
    elif isinstance(data, (int, float, decimal.Decimal)):
        return str(data)
    else:
        return data


def getVehicleId(xid: str) -> int:
    return int(xid.split("-")[1])


async def get_fuel_info(vehicle_id: str, efficiency_type: str):
    if efficiency_type not in ["average", "maximum", "minimum"]:
        raise ValueError(
            "Invalid efficiency type. Must be in 'average', 'minimum' or 'maximum'"
        )
    validate_vehicle_name(vehicle_id)
    logger.info(f"Getting {efficiency_type} fuel efficiency for {vehicle_id}")

    vehicle_id = getVehicleId(vehicle_id)
    cache_key = f"efficiency:mileage:{vehicle_id}:vehicle"
    fuel_efficiency = await hgetall(cache_key)

    if fuel_efficiency:
        logger.debug(f"{cache_key} cache hit")
        return extract_efficiency_type(fuel_efficiency, efficiency_type)

    query = (
        f"SELECT * FROM fuelefficiencybyvehicle WHERE vehicle_id='{vehicle_id}' LIMIT 1"
    )

    fuel_efficiency = {}
    try:
        async with database.pool.acquire() as connection:
            results = await connection.fetchrow(query)
            if results:
                fuel_efficiency = dict(results)
            fuel_efficiency = convert_numbers_to_string(fuel_efficiency)
            await hset(cache_key, fuel_efficiency)
            return extract_efficiency_type(fuel_efficiency, efficiency_type)
    except asyncpg.PostgresError as e:
        logger.debug(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.debug(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




async def get_usage_info(vehicle_id: str):
    validate_vehicle_name(vehicle_id)
    logger.info(f"Getting usage info for {vehicle_id}")

    vehicle_id = getVehicleId(vehicle_id)
    cache_key = f"usage:distance:fuel:{vehicle_id}:vehicle"
    usage_info = await hgetall(cache_key)

    if usage_info:
        logger.debug(f"{cache_key} cache hit")
        return usage_info

    query = (
        f"SELECT * FROM pasttripsbyvehicle WHERE vehicle_id='{vehicle_id}' LIMIT 1"
    )
    usage_info = {}
    try:
        async with database.pool.acquire() as connection:
            results = await connection.fetchrow(query)
            if results:
                usage_info = dict(results)
            usage_info = convert_numbers_to_string(usage_info)
            await hset(cache_key, usage_info)
            return usage_info
    except asyncpg.PostgresError as e:
        logger.debug(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.debug(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")