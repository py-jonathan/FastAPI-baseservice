import openai
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from config import app_config
from utils.security import get_current_user
from models.users import User
import os

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

class AIModelRequest(BaseModel):
    model: str
    message: str

@router.post("/chat")
async def chat_with_ai(request: AIModelRequest, user: User = Depends(get_current_user)):
    if request.model not in ["gpt-3.5-turbo", "gpt-4"]:
        raise HTTPException(status_code=400, detail="Invalid AI model")
    
    try:
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=[{"role": "user", "content": request.message}]
        )
        return {"message": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))