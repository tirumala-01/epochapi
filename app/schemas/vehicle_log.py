from typing import Optional
from datetime import date
from pydantic import BaseModel


class Vehicle(BaseModel):
    id: int
    full_id: str
    name: str
    total_mileage: float


class VehicleLogBase(BaseModel):
    full_id: str
    vehicle_id: int
    vehicle_full_id: str
    trip_date: date


class VehicleLog(VehicleLogBase):
    id: int
    vehicle: VehicleLogBase
    mileage: Optional[float] = None
    fuel_used: Optional[float] = None


class PastVehicleLog(VehicleLogBase):
    id: int
    vehicle: VehicleLogBase
    mileage: float
    fuel_used: float
