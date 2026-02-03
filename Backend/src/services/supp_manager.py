from sqlalchemy.exc import OperationalError
from src.repositories.supp_repo import SuppRepo

from src.services.errors import (
    InvalidInput,
    DatabaseUnavailable,
    SupplementNotFound
)

class SuppManager:
    def __init__(self):
        self.repo = SuppRepo()

    def get_recommendations(self, embedded_symptoms: list[float]) ->list[dict]:
        if not embedded_symptoms:
            raise InvalidInput("Embedding is required")

        try:
            result = self.repo.similarity_search(embedded_symptoms, top_n=5)
        except OperationalError:
            raise DatabaseUnavailable()
        
        return result

    def list_all(self):
        try:
            result = self.repo.get_all()
        except OperationalError:
            raise DatabaseUnavailable() 
        
        return {
            "status": "ok",
            "data": result
        }

    def get_one(self, name: str):
        if not name:
            raise InvalidInput("Name is required")

        try:
            result = self.repo.get_by_name(name)
        except OperationalError:
            raise DatabaseUnavailable()

        if not result:
            raise SupplementNotFound()

        return {
            "status": "ok",
            "data": result
        }
