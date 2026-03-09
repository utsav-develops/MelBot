# app/services/reminder_service.py
import asyncio
import json
from app.schemas.reminder import Reminder
from app.services.push_service import send_push
from app.core.agent_model import generate_structured

def extract_reminder_from_message(message: str) -> dict | None:
    prompt = f"""
    Analyze this message and determine if the user wants to set a reminder.
    
    Message: "{message}"
    
    If it IS a reminder, respond with ONLY this JSON:
    {{"is_reminder": true, "task": "what to remind", "delay_minutes": 10, "confirmation": "Sure! I'll remind you in 10 minutes 💧"}}
    
    If it is NOT a reminder, respond with ONLY:
    {{"is_reminder": false}}
    
    Rules:
    - Convert hours to minutes
    - No time mentioned = 5 minutes default
    - RAW JSON only. No markdown. No extra text.
    """

    raw = generate_structured(prompt)
    print(f"Agent raw output: {raw}")

    try:
        clean = raw.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception as e:
        print(f"Agent parse failed: {e}, raw output was: {raw}")
        return None

async def schedule_reminder(reminder: Reminder):
    asyncio.create_task(_send_after_delay(reminder))
    print(f"Reminder scheduled: '{reminder.message}' in {reminder.delay} min")

async def _send_after_delay(reminder: Reminder):
    await asyncio.sleep(reminder.delay * 60)
    await send_push(
        message=reminder.message,
        title="Mel Reminder 🤖"
    )
    print(f"Reminder fired: {reminder.message}")