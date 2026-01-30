from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.services.chat_manager import ChatManager
from src.dependencies import get_token_provider

router = APIRouter(prefix="/chat")

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    answer: str

@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    payload: dict = Depends(get_token_provider().verify_token)
):
    manager = ChatManager()
    answer = manager.handle_message(
        user_id=payload["user_id"],
        text=req.text
    )
    return ChatResponse(answer=answer)
