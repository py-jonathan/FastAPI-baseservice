from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import List

class Message(BaseModel):
    text: str
    timestamp: datetime

class Conversation(Document):
    user_id: str
    messages: List[Message]
