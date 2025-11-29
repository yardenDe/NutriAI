from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jwt_handler import generate_token, verify_token
from db import add_user, authenticate_user

def setup_user_routes(app: FastAPI):

    class UserRequest(BaseModel):
        unique_name: str
        password: str

    @app.post("/register")
    async def register(req: UserRequest):

        user_id = add_user(req.unique_name, req.password)
        if user_id is None:
            raise HTTPException(status_code=400, detail="User already exists")

        return {"status": "ok"}

    @app.post("/login")
    async def login(req: UserRequest):

        user_id = authenticate_user(req.unique_name, req.password)

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = generate_token(user_id, req.unique_name)
        return {"status": "ok", "token": token}

    @app.get("/user")
    async def get_user(payload: dict = Depends(verify_token)):
        return {
            "user_id": payload["user_id"],
            "username": payload["username"]
        }
