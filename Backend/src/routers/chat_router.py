from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.services.chat_manager import ChatManager
from src.services.errors import (
    InvalidInput,
    DatabaseUnavailable,
    LLMUnavailable
)
from src.dependencies import get_token_provider

router = APIRouter(prefix="/chat")

class ChatRequest(BaseModel):
    text: str

@router.post("")
async def chat(
    req: ChatRequest,
    payload: dict = Depends(get_token_provider().verify_token)
):
    manager = ChatManager()
    try:
        return manager.handle_message(
            user_id=payload["user_id"],
            text=req.text
        )
    except InvalidInput as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LLMUnavailable:
        raise HTTPException(status_code=502, detail="LLM unavailable")
    except DatabaseUnavailable:
        raise HTTPException(status_code=503, detail="Database unavailable")
