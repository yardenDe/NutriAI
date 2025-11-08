import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os


load_dotenv()


secret_key = os.getenv("SECRET_KEY")
algorithm = "HS256"
token_expire = 30

def generate_token(user_id: int, name: str):
     payload = {
        "user_id": user_id,
        "username": name,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token