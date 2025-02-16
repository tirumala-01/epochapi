from fastapi import APIRouter
from .delivery_time import router as delivery_time
from .route_cost import router as route_cost
from .total_shipment_cost import router as total_shipment_cost
from .cities import router as cities

router = APIRouter()


router.include_router(delivery_time, prefix="/shipments")
router.include_router(route_cost, prefix="/shipments")
router.include_router(total_shipment_cost, prefix="/shipments")
router.include_router(cities, prefix="/shipments")
