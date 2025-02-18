import datetime
import decimal
import re
from typing import Any, Union
from loguru import logger
from app.commons.postgres import database as db
from app.commons.redis_helper import hgetall, hset

pattern = r"^(?:[LS]-(0[0-9]{5}|[1-9][0-9]{5})|V-(0[0-9]{2}|[1-9][0-9]{2}))$"


def get_extracted_id(id: Union[str, int]) -> int:
    if isinstance(id, str):
        return int(id.split("-")[1])
    elif isinstance(id, int):
        return id


def convert_numbers_to_string(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: convert_numbers_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numbers_to_string(item) for item in data]
    elif isinstance(
        data, (int, float, decimal.Decimal, datetime.date, datetime.datetime)
    ):
        return str(data)
    else:
        return data


async def get_vehicle_data(id: Union[str, int]):
    id = get_extracted_id(id)
    cache_key = f"vehicle:{id}:details"
    vehicle = await hgetall(cache_key)
    if vehicle:
        logger.debug(f"vehicle {id} cache hit")
        return vehicle
    else:
        logger.debug(f"vehicle {id} cache miss")
        vehicle = await db.get_vehicle_by_id(id)
        if vehicle:
            vehicle = convert_numbers_to_string(dict(vehicle))
            await hset(cache_key, vehicle)
            return vehicle
        else:
            return {"vehicle": "notfound"}


async def get_vehicle_log_data(id: Union[str, int]):
    id = get_extracted_id(id)
    cache_key = f"log:{id}:details"
    log = await hgetall(cache_key)
    if log:
        logger.debug(f"Log {id} cache hit")
        vehicle = await get_vehicle_data(log["vehicle_id"])
        return {**vehicle, **log}
    else:
        logger.debug(f"Log {id} cache miss")
        log = await db.get_log_by_id(id)
        if log:
            vehicle = await get_vehicle_data(log["vehicle_id"])
            log = convert_numbers_to_string(dict(log))
            await hset(cache_key, log)
            return {**vehicle, **log}
        else:
            return {"log": "notfound"}


async def get_shipment_data(id: Union[str, int]):
    id = get_extracted_id(id)
    cache_key = f"shipment:{id}:details"
    shipment = await hgetall(cache_key)
    if shipment:
        logger.debug(f"shipment {id} cache hit")
        log = await get_vehicle_log_data(shipment["log_id"])
        return {**shipment, **log}
    else:
        logger.debug(f"shipment {id} cache miss")
        shipment = await db.get_shipment_by_id(id)
        if shipment:
            log = await get_vehicle_log_data(shipment["log_id"])
            shipment = convert_numbers_to_string(dict(shipment))
            await hset(cache_key, shipment)
            return {**shipment, **log}
        else:
            return {"shipment": "notfound"}


async def get_id_info(id: str):
    logger.info(f"Getting info for {id}")
    try:
        match = re.match(pattern, id)
        if match:
            if match.group(0).startswith("S-"):
                return await get_shipment_data(id)
            elif match.group(0).startswith("L-"):
                return await get_vehicle_log_data(id)
            elif match.group(0).startswith("V-"):
                return await get_vehicle_data(id)
        else:
            logger.error(f"Invalid Id {id}")
            raise ValueError("Invalid Id")
    except Exception as e:
        raise
