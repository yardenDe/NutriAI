import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def _get_client():
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("LLM_API_KEY not found in environment")

    model = os.getenv("LLM_MODEL", "gemini-2.0-flash")
    client = genai.Client(api_key=api_key)
    return client, model

def _build_prompt(user_text: str, context: list[str]) -> str:
    context_text = "\n".join(context) if context else "No prior context."

    return f"""
You are a helpful assistant.

Conversation context:
{context_text}

User message:
{user_text}

Assistant:
""".strip()

def generate_answer(user_text: str, context: list[str]) -> str:
    """
    Public API:
    Send input to the LLM and return a text answer.
    """
    client, model = _get_client()
    prompt = _build_prompt(user_text, context)

    chat = client.chats.create(model=model)
    response = chat.send_message(prompt)

    return response.text.strip()
