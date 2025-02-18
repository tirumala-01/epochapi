from fastapi import APIRouter, HTTPException
from loguru import logger
from app.crud.search import get_id_info

router = APIRouter(prefix="/search")


@router.get("")
async def get_details(id: str):
    try:
        return await get_id_info(id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValueError as e:
        logger.error(f"Value error getting info {id}: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
    except Exception as e:
        logger.error(f"Error getting info {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
