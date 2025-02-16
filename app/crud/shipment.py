import asyncpg
from app.commons.postgres import database
from app.schemas.shipment import HighestShipmentCost, LowestShipmentCost


async def origin_cities():
    query = "select * from origincities"
    shipment_origins = []
    try:
        async with database.pool.acquire() as connection:
            try:
                results = await connection.fetch(query)
                for record in results:
                    shipment_origins.append(record["shipment_origin"])
            except asyncpg.PostgresError as e:
                print(f"Database error: {e}")
                return []
            except Exception as e:
                print(f"Error: {e}")
                return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    return shipment_origins


async def destination_cities():
    query = "select * from DestinationCities"
    shipment_destinations = []
    try:
        async with database.pool.acquire() as connection:
            try:
                results = await connection.fetch(query)
                for record in results:
                    shipment_destinations.append(record["shipment_destination"])
            except asyncpg.PostgresError as e:
                print(f"Database error: {e}")
                return []
            except Exception as e:
                print(f"Error: {e}")
                return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    return shipment_destinations


async def get_high_ship_cost():
    query = "select * from HighestShipmentCost"
    shipment_costs = []
    try:
        async with database.pool.acquire() as connection:
            try:
                results = await connection.fetch(query)
                for record in results:
                    shipment_costs.append(
                        HighestShipmentCost(
                            route_id=record["route_id"],
                            origin=record["origin"],
                            destination=record["destination"],
                            total_shipment_cost=record["total_shipment_cost"],
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


async def get_low_ship_cost():
    query = "select * from LowestShipmentCost"
    shipment_costs = []
    try:
        async with database.pool.acquire() as connection:
            try:
                results = await connection.fetch(query)
                for record in results:
                    shipment_costs.append(
                        LowestShipmentCost(
                            route_id=record["route_id"],
                            origin=record["origin"],
                            destination=record["destination"],
                            total_shipment_cost=record["total_shipment_cost"],
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
