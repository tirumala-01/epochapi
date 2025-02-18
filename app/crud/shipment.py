import json
import asyncpg
from loguru import logger
from app.commons.postgres import database as db
from app.commons.redis_helper import rpush, lrangeall, set, get, hgetall, hset
from typing import List, Dict, Any
from .util import validate_city_names, convert_numbers_to_string, extract_metric


async def get_city_names(city_type: str) -> List[str]:
    logger.info(f"Getting {city_type} cities")
    cache_key = f"citylist:{city_type}"
    results = await lrangeall(cache_key)

    if results:
        logger.debug(f"{cache_key} cache hit")
        return results

    logger.debug("city_type cache miss")
    query = f"SELECT * FROM {city_type}cities"

    shipment_cities = []
    results = await db.fetch_rows(query)
    if results:
        for record in results:
            shipment_cities.append(record[f"shipment_{city_type}"])
        await rpush(cache_key, shipment_cities)
    return shipment_cities


async def get_total_ship_cost(cost_type: str) -> List[Dict[str, Any]]:
    logger.info(f"Getting {cost_type} expensive routes")
    cache_key = f"expensivecities:{cost_type}"
    results = await get(cache_key)

    if results:
        logger.debug(f"{cache_key} cache hit")
        return json.loads(results)

    query = f"SELECT * FROM {cost_type}shipmentcost"
    shipment_costs = []
    results = await db.fetch_rows(query)
    if results:
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
        return shipment_costs
    else:
        return {"routes": "notfound"}


async def get_ship_cost(origin: str, destination: str, cost_type: str):
    validate_city_names(origin, destination)
    logger.debug(f"Getting {cost_type} shipment costs for {origin}-{destination}")

    route_id = f"{origin}-{destination}"
    cache_key = f"routecost:{route_id}:details".replace(" ", "")
    results = await hgetall(cache_key)

    if results:
        logger.debug(f"{cache_key} cache hit")
        return extract_metric(results, cost_type, "shipment_cost")

    results = await db.get_shipment_cost_city(route_id)
    if results:
        results = convert_numbers_to_string(dict(results))
        await hset(cache_key, results)
        return extract_metric(results, cost_type, "shipment_cost")
    else:
        return {"cost": "notfound"}


async def get_ship_time(origin: str, destination: str, operation: str):
    validate_city_names(origin, destination)
    logger.debug(f"Getting {operation} shipment time for {origin}-{destination}")

    route_id = f"{origin}-{destination}"
    cache_key = f"deliverytime:{route_id}:details".replace(" ", "")
    results = await hgetall(cache_key)

    if results:
        logger.debug(f"{cache_key} cache hit")
        return extract_metric(results, operation, "delivery_time")

    results = await db.get_shipment_time_city(route_id)
    if results:
        results = convert_numbers_to_string(dict(results))
        await hset(cache_key, results)
        return extract_metric(results, operation, "delivery_time")
    else:
        return {"route": "notfound"}
