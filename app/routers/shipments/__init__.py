from fastapi import APIRouter
from .delivery_time import router as delivery_time
from .route_cost import router as route_cost
from .expensive_routes import router as expensive_routes
from .cities import router as cities

router = APIRouter()


router.include_router(delivery_time, prefix="/shipments")
router.include_router(route_cost, prefix="/shipments")
router.include_router(expensive_routes, prefix="/shipments")
router.include_router(cities, prefix="/shipments")
