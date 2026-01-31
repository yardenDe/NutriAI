from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.user_manager import UserManager
from src.services.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    DatabaseUnavailable
)

router = APIRouter(prefix="/users")

manager = UserManager()

class UserRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(req: UserRequest):
    try:
        return manager.register(req.username, req.password)

    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail="User already exists")

    except DatabaseUnavailable:
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.post("/login")
def login(req: UserRequest):
    try:
        result = manager.login(req.username, req.password)
        return result

    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except DatabaseUnavailable:
        raise HTTPException(status_code=503, detail="Service unavailable")
