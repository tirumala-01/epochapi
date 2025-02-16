import asyncpg
from loguru import logger
from app.commons.postgres import database
from app.schemas.shipment import ShipmentCost


async def get_city_names(city_type):
    if city_type not in ["origin", "destination"]:
        raise ValueError("Invalid cost type. Must be 'origin' or 'destination'")
    query = f"select * from {city_type}cities"
    shipment_origins = []
    try:
        async with database.pool.acquire() as connection:
            try:
                results = await connection.fetch(query)
                for record in results:
                    shipment_origins.append(record[f"shipment_{city_type}"])
            except asyncpg.PostgresError as e:
                print(f"Database error: {e}")
                return []
            except Exception as e:
                print(f"Error1 : {e}")
                return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    return shipment_origins


async def get_total_ship_cost(cost_type):
    if cost_type not in ["highest", "lowest"]:
        raise ValueError("Invalid cost type. Must be 'highest' or 'lowest'")

    query = f"select * from {cost_type}shipmentcost"
    shipment_costs = []
    try:
        async with database.pool.acquire() as connection:
            try:
                results = await connection.fetch(query)
                for record in results:
                    shipment_costs.append(
                        ShipmentCost(
                            route_id=record["route_id"],
                            origin=record["origin"],
                            destination=record["destination"],
                            total_shipment_cost=record["total_shipment_cost"],
                            type=cost_type.capitalize()
                        )
                    )
            except asyncpg.PostgresError as e:
                print(f"Database error: {e}")
                return []
            except Exception as e:
                print(f"Error: {e}")
                return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    return shipment_costs


async def get_ship_cost(cost_type):
    return ''