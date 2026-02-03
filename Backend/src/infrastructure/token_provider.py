import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()


class TokenProvider:
    """
    Handles JWT creation and validation.
    """

    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "mysecretkey")
        self.algorithm = "HS256"
        self.expire_minutes = 30
        self.security = HTTPBearer()

    def generate_token(self, user_id: int, user_name: str) -> str:
        payload = {
            "user_id": user_id,
            "username": user_name,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.expire_minutes),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(
        self, credentials: HTTPAuthorizationCredentials
    ) -> dict:
        token = credentials.credentials
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
