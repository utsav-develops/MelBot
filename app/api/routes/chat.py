import asyncio
from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage, UsageInfo
from app.services.chat_service import handle_chat
from app.services.reminder_service import extract_reminder_from_message, schedule_reminder
from app.schemas.reminder import Reminder
from starlette.concurrency import run_in_threadpool

router = APIRouter()

REMINDER_KEYWORDS = [
    "remind",
    "reminder",
    "don't let me forget",
    "dont let me forget",
    "ping me",
    "alert me",
    "notify me",
    "don't forget",
    "dont forget",
    "remember to",
    "set a reminder",
    "wake me",
    "tell me later",
    "let me know in",
]

def looks_like_reminder(message: str) -> bool:
    lowered = message.lower()
    return any(kw in lowered for kw in REMINDER_KEYWORDS)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    if looks_like_reminder(request.message):
        print(f"Reminder keyword detected — running agent model")
        reminder_data = await run_in_threadpool(
            extract_reminder_from_message, request.message
        )
        print(f"Agent decision: {reminder_data}")

        if reminder_data and reminder_data.get("is_reminder"):
            asyncio.create_task(
                schedule_reminder(Reminder(
                    message=f"⏰ {reminder_data['task']}",
                    delay=reminder_data["delay_seconds"],
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
    
    
    print("No reminder detected — passing to Mel")
    return await run_in_threadpool(handle_chat, request)