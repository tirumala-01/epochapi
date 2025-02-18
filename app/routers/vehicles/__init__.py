from fastapi import APIRouter
from .fuel_efficiency import router as fuel_efficiency
from .total_usage import router as total_usage


router = APIRouter()


router.include_router(fuel_efficiency, prefix="/vehicles")
router.include_router(total_usage, prefix="/vehicles")
