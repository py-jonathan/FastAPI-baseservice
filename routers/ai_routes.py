from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.auth import get_current_user
from models.users import User
from endpoints.ai import chat_with_ai

router = APIRouter()

class AIModelRequest(BaseModel):
    model: str
    message: str

@router.post("/chat")
async def ai_chat_endpoint(request: AIModelRequest, user: User = Depends(get_current_user)):
    if request.model not in ["gpt-3.5-turbo", "gpt-4"]:
        raise HTTPException(status_code=400, detail="Invalid AI model")
    
    try:
        return await chat_with_ai(request.model, request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
