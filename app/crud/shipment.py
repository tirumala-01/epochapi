import decimal
import re
import json
import asyncpg
from loguru import logger
from app.commons.postgres import database
from app.commons.redis_helper import rpush, lrangeall, set, get, hgetall, hset
from typing import List, Dict, Any


def validate_city_names(origin: str, destination: str) -> None:
    city_re = "^(?=[a-zA-Z])[a-zA-Z ]+$"
    if not (re.match(city_re, origin) and re.match(city_re, destination)):
        logger.error(f"Invalid origin or destination {origin}-{destination}")
        raise ValueError("Invalid origin or destination")


def extract_delivery_time(data: Dict[str, Any], metric: str) -> Dict[str, Any]:
    valid_metrics = {
        "average": "avg_delivery_time",
        "maximum": "max_delivery_time",
        "minimum": "min_delivery_time",
        "total": "total_delivery_time",
    }
    metric_key = valid_metrics[metric]
    filtered_entry = {
        key: value
        for key, value in data.items()
        if key in {"route_id", "origin", "destination", "total_trips", metric_key}
    }
    return filtered_entry


async def get_city_names(city_type: str) -> List[str]:
    if city_type not in ["origin", "destination"]:
        raise ValueError("Invalid cost type. Must be 'origin' or 'destination'")

    cache_key = f"{city_type}_cities"
    shipment_cities = await lrangeall(cache_key)

    if shipment_cities:
        logger.debug(f"{cache_key} cache hit")
        return shipment_cities

    logger.debug("city_type cache miss")
    query = f"SELECT * FROM {city_type}cities"

    shipment_cities = []
    async with database.pool.acquire() as connection:
        try:
            results = await connection.fetch(query)
            for record in results:
                shipment_cities.append(record[f"shipment_{city_type}"])
            await rpush(cache_key, shipment_cities)
        except asyncpg.PostgresError as e:
            logger.debug(f"Database error: {e}")
            return []
        except Exception as e:
            logger.debug(f"Error: {e}")
            return []
    return shipment_cities


def convert_numbers_to_string(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: convert_numbers_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numbers_to_string(item) for item in data]
    elif isinstance(data, (int, float, decimal.Decimal)):
        return str(data)
    else:
        return data


def get_cache_key(key: str) -> str:
    return key.replace(" ", "")


async def get_total_ship_cost(cost_type: str) -> List[Dict[str, Any]]:
    if cost_type not in ["highest", "lowest"]:
        raise ValueError("Invalid cost type. Must be 'highest' or 'lowest'")

    cache_key = f"expensive_cities:{cost_type}"
    shipment_costs = await get(cache_key)

    if shipment_costs:
        logger.debug(f"{cache_key} cache hit")
        return json.loads(shipment_costs)

    query = f"SELECT * FROM {cost_type}shipmentcost"
    shipment_costs = []
    async with database.pool.acquire() as connection:
        try:
            results = await connection.fetch(query)
            for record in results:
                shipment_costs.append(
                    {
                        "route_id": record["route_id"],
                        "origin": record["origin"],
                        "destination": record["destination"],
                        "total_shipment_cost": str(record["total_shipment_cost"]),
                        "type": cost_type.capitalize(),
                    }
                )
            await set(cache_key, json.dumps(shipment_costs))
        except asyncpg.PostgresError as e:
            logger.debug(f"Database error: {e}")
            return []
        except Exception as e:
            logger.debug(f"Error: {e}")
            return []
    return shipment_costs


async def get_ship_cost(
    origin: str, destination: str, cost_type: str
) -> Dict[str, Any]:
    if cost_type not in ["average", "maximum", "minimum", "total"]:
        raise ValueError(
            "Invalid cost type. Must be in 'average', 'minimum', 'maximum' or 'total'"
        )

    validate_city_names(origin, destination)
    logger.info(f"Getting {cost_type} shipment costs for {origin}-{destination}")

    route_id = f"{origin}-{destination}"
    cache_key = get_cache_key(f"shipment:cost:{route_id}")
    delivery_time = await hgetall(cache_key)

    if delivery_time:
        logger.debug(f"{cache_key} cache hit")
        return extract_delivery_time(delivery_time, cost_type)

    query = f"SELECT * FROM deliverytimesbyroute WHERE route_id='{route_id}' LIMIT 1"
    delivery_time = {}

    async with database.pool.acquire() as connection:
        try:
            results = await connection.fetchrow(query)
            if results:
                delivery_time = dict(results)
            delivery_time = convert_numbers_to_string(delivery_time)
            await hset(cache_key, delivery_time)
            return extract_delivery_time(delivery_time, cost_type)
        except asyncpg.PostgresError as e:
            logger.debug(f"Database error: {e}")
            return {}
        except Exception as e:
            logger.debug(f"Error: {e}")
            return {}

    return {}
