from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jwt_handler import generate_token, verify_token  

def setup_user_routes(app: FastAPI):
    DB = {}
    NEXT_ID = 1

    class UserRequest(BaseModel):
        unique_name: str
        password: str

    @app.post("/register")
    async def register(req: UserRequest):
        print("Request body:", req)

        nonlocal NEXT_ID
        if req.unique_name in DB:
            raise HTTPException(status_code=400, detail="User exists")
        DB[req.unique_name] = {"id": NEXT_ID, "password": req.password}
        NEXT_ID += 1
        return {"status": "ok"}

    @app.post("/login")
    async def login(req: UserRequest):
        if req.unique_name not in DB:
            raise HTTPException(status_code=404, detail="User not found")

        if DB[req.unique_name]["password"] != req.password:
            raise HTTPException(status_code=401, detail="Invalid password")

        user_id = DB[req.unique_name]["id"]
        token = generate_token(user_id, req.unique_name)
        return {"status": "ok", "token": token}

    @app.get("/user")
    async def get_user(payload: dict = Depends(verify_token)):
        return {
            "user_id": payload["user_id"],
            "username": payload["username"]
        }
