from sqlalchemy.exc import IntegrityError, OperationalError

from src.repositories.user_repo import UserRepo
from src.services.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    DatabaseUnavailable,
)

class UserManager:
    def __init__(self, token_provider):
        self.repo = UserRepo()
        self.token_provider = token_provider

    def register(self, username: str, password: str):
        try:
            self.repo.add_user(username, password)
        except IntegrityError:
            raise UserAlreadyExists()
        except OperationalError:
            raise DatabaseUnavailable()

        return {
            "status": "ok",
            "message": "User created successfully",
        }

    def login(self, username: str, password: str):
        try:
            user = self.repo.get_user(username)
        except OperationalError:
            raise DatabaseUnavailable()

        if not user or user["password"] != password:
            raise InvalidCredentials()

        token = self.token_provider.generate_token(
            user_id=user["id"],
            user_name=username
        )

        return {
            "status": "ok",
            "token": token
        }
