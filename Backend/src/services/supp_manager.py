from src.repositories.supp_repo import SuppRepo
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import numpy as np


class SuppManager:
    def __init__(self):
        self.repo = SuppRepo()

        load_dotenv()

        model_name = os.getenv(
            "EMBEDDING_MODEL",
            "all-MiniLM-L6-v2"
        )

        self.model = SentenceTransformer(model_name)

    def get_recommendations(self, symptoms: list[str]):
        query_text = " ".join(symptoms)

        embedding: np.ndarray = self.model.encode(query_text)
        embedding_for_db = embedding.tolist()

        return self.repo.get_by_similarity(
            embedding_for_db,
            top_n=5
        )

    def list_all(self):
        return self.repo.get_all()

    def get_one(self, name: str):
        return self.repo.get_by_name(name)
    