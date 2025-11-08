from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jwt_handler import generate_token, verify_token  

def setup_user_routes(app: FastAPI):
    DB = {}
    NEXT_ID = 1

    class UserRequest(BaseModel):
        uniqe_name: str
        password: str

    @app.post("/register")
    async def register(req: UserRequest):
        nonlocal NEXT_ID
        if req.uniqe_name in DB:
            raise HTTPException(status_code=400, detail="User exists")
        DB[req.uniqe_name] = {"id": NEXT_ID, "password": req.password}
        NEXT_ID += 1
        return {"status": "ok"}

    @app.post("/login")
    async def login(req: UserRequest):
        if req.uniqe_name not in DB or DB[req.uniqe_name]["password"] != req.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = DB[req.uniqe_name]["id"]
        token = generate_token(user_id, req.uniqe_name)
        return {"token": token}

    @app.get("/user")
    async def get_user(payload: dict = Depends(verify_token)):
        return {
            "user_id": payload["user_id"],
            "username": payload["username"]
        }
