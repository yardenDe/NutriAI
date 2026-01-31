from sqlalchemy.exc import OperationalError
from src.repositories.supp_repo import SuppRepo
from src.dependencies import get_embedding_model
import numpy as np

from src.services.errors import (
    InvalidInput,
    EmbeddingError,
    DatabaseUnavailable,
    SupplementNotFound
)

class SuppManager:
    def __init__(self):
        self.repo = SuppRepo()
        self.model = get_embedding_model()

    def get_recommendations(self, symptoms: list[str]):
        if not symptoms:
            raise InvalidInput()

        query_text = " ".join(symptoms)
        try:
            embedding: np.ndarray = self.model.encode(query_text)
        except Exception as e:
            raise EmbeddingError("Failed to generate embedding") from e

        embedding_for_db = embedding.tolist()
        try:
            result = self.repo.get_by_similarity(embedding_for_db, top_n=5)
        except OperationalError:
            raise DatabaseUnavailable()
        
        return {
            "status": "ok",
            "data": result
        }


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
