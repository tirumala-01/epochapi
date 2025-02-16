from pydantic import BaseModel


class Vehicle(BaseModel):
    vehicle_id: int
    vehicle_full_id: str
    vehicle_name: str
    vehicle_total_mileage: float
