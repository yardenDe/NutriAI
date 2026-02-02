from sentence_transformers import SentenceTransformer
import os
from google import genai
from dotenv import load_dotenv

from src.infrastructure.db_manager import DBManager
from src.infrastructure.token_provider import TokenProvider
from src.infrastructure.llm_manager import LLMManager
from src.infrastructure.embeddings import Embeddings


_db_manager = None
_token_provider = None
_embedding_model = None
_llm_manager = None

load_dotenv()

def get_db_manager() -> DBManager:
    global _db_manager

    if _db_manager is None:
        database_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
        _db_manager = DBManager(database_url)

    return _db_manager


def get_token_provider():
    global _token_provider
    
    if _token_provider is None:
        _token_provider = TokenProvider()
    return _token_provider


def get_embedding() -> Embeddings:
    global _embedding_model

    if _embedding_model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        model = SentenceTransformer(model_name)
        _embedding_model = Embeddings(model)
    return _embedding_model


def get_llm() -> LLMManager:
    global _llm_manager

    if _llm_manager is None:
        api_key = os.getenv("LLM_API_KEY")
        model = os.getenv("LLM_MODEL", "gemini-2.0-flash")

        if not api_key:
            raise RuntimeError("LLM_API_KEY not set")

        client = genai.Client(api_key=api_key)
        _llm_service = LLMManager(client=client, model=model)

    return _llm_service
