from fastapi import FastAPI
from pydantic import BaseModel

def setup_user_routes(app: FastAPI):
    DB = {}

    class UserRequest(BaseModel):
        uniqe_name: str
        password: str

    @app.post("/register")
    async def register(req: UserRequest):
        if req.uniqe_name in DB:
            return {"status": "user exists"}
        DB[req.uniqe_name] = req.password
        return {"status": "ok"}

    @app.post("/login")
    async def login(req: UserRequest):
        name = req.uniqe_name
        password = req.password
        if name not in DB:
            return {"status": "User not found"}
        if DB[name] != password:
            return {"status": "Invalid Password"}
        
        return generate_token(name)

    def generate_token(name: str):
        token = "xyz"
        return {"status": "ok", "token": token}

    
    @app.get("/user")
    async def user():
        pass
