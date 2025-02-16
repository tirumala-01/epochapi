from pydantic import BaseModel


class Shipment(BaseModel):
    shipment_id: int
    shipment_full_id: str
    shipment_origin: str
    shipment_destination: str
    shipment_weight: float
    shipment_cost: float
    shipment_delivery_time: int
    shipment_log_id: int
    shipment_full_log_id: str


class PastShipment(BaseModel):
    shipment_id: int
    shipment_full_id: str
    shipment_origin: str
    shipment_destination: str
    shipment_weight: float
    shipment_cost: float
    shipment_delivery_time: int
    shipment_log_id: int
    shipment_full_log_id: str
    shipment_route_id: str

class DeliveryTimesByRoute(BaseModel):
    route_id: str
    origin: str
    destination: str
    avg_delivery_time: float
    max_delivery_time: int
    min_delivery_time: int
    total_delivery_time: int
    total_trips: int


class CostByRoute(BaseModel):
    route_id: str
    origin: str
    destination: str
    avg_shipment_cost: float
    max_shipment_cost: float
    min_shipment_cost: float
    total_shipment_cost: float
    total_trips: int


class HighestShipmentCost(BaseModel):
    route_id: str
    origin: str
    destination: str
    total_shipment_cost: float


class LowestShipmentCost(BaseModel):
    route_id: str
    origin: str
    destination: str
    total_shipment_cost: float