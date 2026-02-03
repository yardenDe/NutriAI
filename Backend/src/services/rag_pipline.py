import json
from typing import Optional

from src.services.supp_manager import SuppManager
from src.dependencies import get_embedding, get_llm
from src.services.prompts import (
    extract_symptoms_prompt,
    answer_with_context_prompt
)

llm_service = get_llm()
embedding_service = get_embedding()
supp_manager = SuppManager()

def extract_symptoms(user_input: str) -> list[str]:
    prompt = extract_symptoms_prompt(user_input)
    raw = llm_service.generate(prompt)
    
    clean_raw = raw.replace("```json", "").replace("```", "").strip()
    
    try:
        symptoms = json.loads(clean_raw)
        if not isinstance(symptoms, list):
            return []
        return [s.strip() for s in symptoms if isinstance(s, str) and s.strip()]
    except (json.JSONDecodeError, TypeError):
        return []

def retrieve_relevant_supplements(symptoms: list[str]) -> list[dict]:
    embedding = embedding_service.to_embedded(symptoms)
    
    if not embedding:
        return []
        
    return supp_manager.get_recommendations(embedding)

def build_augmentation_prompt(user_input: str, supplements: list[dict], chat_context: str) -> str:
    rag_context = json.dumps(supplements, indent=2)
    return answer_with_context_prompt(
        question=user_input,
        rag_context=rag_context,
        chat_context=chat_context
    )

def rag_pipeline(user_input: str, chat_context: str) -> Optional[str]:
    symptoms = extract_symptoms(user_input)
    
    if not symptoms:
        return None

    supplements = retrieve_relevant_supplements(symptoms)
    
    if not supplements:
        return None

    final_prompt = build_augmentation_prompt(user_input, supplements, chat_context)
    
    return llm_service.generate(final_prompt)