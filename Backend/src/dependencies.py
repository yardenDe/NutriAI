from sentence_transformers import SentenceTransformer
import os
from google import genai

from src.infrastructure.db_manager import DBManager
from src.infrastructure.token_provider import TokenProvider

_db = None
_token_provider = None
_embedding_model = None
_llm_client = None
_llm_model = None


def get_db_manager():
    global _db
    if _db is None:
        _db = DBManager()
    return _db


def get_token_provider():
    global _token_provider
    if _token_provider is None:
        _token_provider = TokenProvider()
    return _token_provider


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        _embedding_model = SentenceTransformer(model_name)
    return _embedding_model


def get_llm():
    global _llm_client, _llm_model

    if _llm_client is None:
        api_key = os.getenv("LLM_API_KEY")
        _llm_client = genai.Client(api_key=api_key)

    if _llm_model is None:
        _llm_model = os.getenv("LLM_MODEL", "gemini-2.0-flash")

    return _llm_client, _llm_model
