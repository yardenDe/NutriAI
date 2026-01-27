from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.user_manager import UserManager
from app.dependencies import get_db_manager, get_token_provider

router = APIRouter(prefix="/users")

class UserRequest(BaseModel):
    unique_name: str
    password: str

@router.post("/register")
async def register(req: UserRequest):
    manager = UserManager(get_db_manager(), get_token_provider())
    user_id = manager.register_user(req.unique_name, req.password)
    
    if user_id is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"status": "ok", "user_id": user_id}

@router.post("/login")
async def login(req: UserRequest):
    manager = UserManager(get_db_manager(), get_token_provider())
    token = manager.login_user(req.unique_name, req.password)
    
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "ok", "token": token}