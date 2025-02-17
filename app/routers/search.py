from fastapi import APIRouter, HTTPException
from loguru import logger
# from app.crud.search import search_ship

router = APIRouter(prefix="/search")


@router.get("")
async def get_shipment_information(shipment_id: str):
    try:
        # return await search_ship(shipment_id)
        return
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValueError as e:
        logger.error(f"Value error getting shipment info {shipment_id}: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
    except Exception as e:
        logger.error(f"Error getting shipment info {shipment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
