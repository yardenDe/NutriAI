from fastapi import APIRouter, Query, HTTPException

from src.services.supp_manager import SuppManager
from src.services.errors import (
    InvalidInput,
    EmbeddingError,
    DatabaseUnavailable,
    SupplementNotFound
)

router = APIRouter(prefix="/supplements")


@router.get("/recommendations")
async def recommendations(symptoms: list[str] = Query(...)):
    manager = SuppManager()
    try:
        return manager.get_recommendations(symptoms)
    except InvalidInput as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EmbeddingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseUnavailable:
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.get("")
async def list_supplements():
    manager = SuppManager()
    try:
        return manager.list_all()
    except DatabaseUnavailable:
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.get("/{name}")
async def get_supplement(name: str):
    manager = SuppManager()
    try:
        return manager.get_one(name)
    except InvalidInput as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SupplementNotFound:
        raise HTTPException(status_code=404, detail="Supplement not found")
    except DatabaseUnavailable:
        raise HTTPException(status_code=503, detail="Database unavailable")
