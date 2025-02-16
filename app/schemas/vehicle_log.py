from typing import Optional
from datetime import date
from pydantic import BaseModel


class VehicleLog(BaseModel):
    vl_id: int
    vl_full_id: str
    vl_vehicle_id: int
    vl_vehicle_full_id: str
    vl_trip_date: date
    vl_mileage: Optional[float] = None
    vl_fuel_used: Optional[float] = None


class PastVehicleLog(BaseModel):
    vl_id: int
    vl_full_id: str
    vl_vehicle_id: int
    vl_vehicle_full_id: str
    vl_trip_date: date
    vl_mileage: Optional[float] = None
    vl_fuel_used: Optional[float] = None
