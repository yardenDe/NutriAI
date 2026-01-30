from fastapi import APIRouter, Query, HTTPException
from src.services.supp_manager import SuppManager

router = APIRouter(prefix="/supplements")

@router.get("/recommendations")
async def recommendations(symptoms: list[str] = Query(...)):
    manager = SuppManager()
    return {"recommendations": manager.get_recommendations(symptoms)}

@router.get("")
async def list_supplements():
    manager = SuppManager()
    return manager.list_all()

@router.get("/{name}")
async def get_supplement(name: str):
    manager = SuppManager()
    result = manager.get_one(name)
    if not result:
        raise HTTPException(status_code=404, detail="Supplement not found")
    return result