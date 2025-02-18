from fastapi import APIRouter

from .vehicles import router as vehicles_router
from .shipments import router as shipments_router
from .search import router as search_router

router = APIRouter()

router.include_router(shipments_router, tags=["Shipments"])
router.include_router(vehicles_router, tags=["Vehicles"])
router.include_router(search_router, tags=["Search"])