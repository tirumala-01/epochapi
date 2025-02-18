import asyncpg
from loguru import logger
from ..config import settings


class Postgres:
    def __init__(self):
        self.host = settings.DATABASE_URL
        self._connection_pool = None
        self.con = None

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(self.host)
                self.con = await self._connection_pool.acquire()
            except Exception as e:
                print(e)

    def disconnect(self):
        self._connection_pool.terminate()

    async def fetch_rows(self, query: str):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                result = await con.fetch(query)
                return result
            except Exception as e:
                print(e)
            finally:
                await self._connection_pool.release(con)

    async def get_vehicle_by_id(self, id):
        if not self._connection_pool:
            logger.debug("Connection pool not initialized. Connecting...")
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                logger.debug("Preparing SQL statement...")
                stmt = await con.prepare(
                    "select vehicle_full_id as vehicle_id, vehicle_name, vehicle_total_mileage \
                    from vehicles where vehicle_id = $1"
                )
                logger.debug(f"Executing SQL statement with id: {id}")
                return await stmt.fetchrow(id)
            except Exception as e:
                logger.debug(f"Error: {e}")
            finally:
                await self._connection_pool.release(con)

    async def get_log_by_id(self, id):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                stmt = await con.prepare(
                    "select vl_full_id as full_id, vl_vehicle_full_id as vehicle_id, \
                    vl_trip_date as trip_date, vl_mileage as mileage, vl_fuel_used as \
                    fuel_used from vehicles_logs where vl_id = $1"
                )
                return await stmt.fetchrow(id)
            except Exception as e:
                logger.debug(f"Error: {e}")
            finally:
                await self._connection_pool.release(con)

    async def get_shipment_by_id(self, id):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                stmt = await con.prepare(
                    "select shipment_full_id as shipment_id, shipment_origin as origin, \
                        shipment_destination as destination, shipment_weight as weight, \
                        shipment_cost as cost, shipment_delivery_time as delivery_time, \
                        shipment_full_log_id as log_id from shipments where shipment_id = $1"
                )
                return await stmt.fetchrow(id)
            except Exception as e:
                logger.debug(f"Error: {e}")
            finally:
                await self._connection_pool.release(con)

    async def get_shipment_time_city(self, route):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                stmt = await con.prepare(
                    "SELECT * FROM deliverytimesbyroute WHERE route_id= $1"
                )
                return await stmt.fetchrow(route)
            except Exception as e:
                logger.debug(f"Error: {e}")
            finally:
                await self._connection_pool.release(con)


    async def get_shipment_cost_city(self, route):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                stmt = await con.prepare(
                    "SELECT * FROM costbyroute WHERE route_id= $1"
                )
                return await stmt.fetchrow(route)
            except Exception as e:
                logger.debug(f"Error: {e}")
            finally:
                await self._connection_pool.release(con)

    async def get_vehicle_efficiency(self, route):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                stmt = await con.prepare(
                    "SELECT * FROM fuelefficiencybyvehicle WHERE vehicle_id= $1"
                )
                return await stmt.fetchrow(route)
            except Exception as e:
                logger.debug(f"Error: {e}")
            finally:
                await self._connection_pool.release(con)

    async def get_vehicle_fuelmileage(self, route):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                stmt = await con.prepare(
                    "SELECT * FROM pasttripsbyvehicle WHERE vehicle_id= $1"
                )
                return await stmt.fetchrow(route)
            except Exception as e:
                logger.debug(f"Error: {e}")
            finally:
                await self._connection_pool.release(con)


database = Postgres()
