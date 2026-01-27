from src.db_repo.supp_repo import SuppRepo
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

class SupplementManager:
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
        emb_list = self.model.encode(query_text).tolist()
        embedded_goal = "[" + ",".join(str(x) for x in emb_list) + "]"
        return self.repo.find_similar(embedded_goal, top_n=5)

    def list_all(self):
        return self.repo.get_all()

    def get_one(self, name: str):
        results = self.repo.get_by_name(name)
        return results[0] if results else None