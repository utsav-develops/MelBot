import asyncio
from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage, UsageInfo
from app.services.chat_service import handle_chat
from app.services.reminder_service import extract_reminder_from_message, schedule_reminder
from app.schemas.reminder import Reminder

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    reminder_data = extract_reminder_from_message(request.message)
    
    if reminder_data and reminder_data.get("is_reminder"):
        asyncio.create_task(
            schedule_reminder(Reminder(
                message=f"⏰ {reminder_data['task']}",
                delay=reminder_data["delay_minutes"],
            ))
        )
        
        return ChatResponse(
            message=ChatMessage(
                role="assistant",
                content=reminder_data["confirmation"]
            ),
            usage=UsageInfo(
                promptTokens=0,
                completionTokens=0,
                totalTokens=0,
            )
        )
    
    
    return handle_chat(request)