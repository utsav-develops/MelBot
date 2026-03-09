from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str        # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ChatMessage(BaseModel):
    role: str
    content: str

class UsageInfo(BaseModel):
    promptTokens: int
    completionTokens: int
    totalTokens: int

class ChatResponse(BaseModel):
    message: ChatMessage
    usage: UsageInfo

class ChatHistory(BaseModel):
    id: str
    messages: ChatMessage
    createdAt: str
    updatedAt: str