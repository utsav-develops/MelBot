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
    {{"is_reminder": true, "task": "what to remind", "delay_seconds": 600, "confirmation": "Sure! I'll remind you in 10 minutes 💧"}}
    
    If it is NOT a reminder, respond with ONLY:
    {{"is_reminder": false}}
    
    Rules:
    - Always convert to seconds:
        "30 seconds" = 30
        "2 minutes"  = 120
        "1 hour"     = 3600
        "2 hours"    = 7200
    - If user says a specific time like "at 3pm" calculate seconds from now
    - No time mentioned = 300 seconds default (5 minutes)
    - confirmation should naturally mention the time in human format
      e.g. "in 30 seconds", "in 2 minutes", "in 1 hour"
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
    # create_task fires and forgets — doesn't block the response
    asyncio.create_task(_send_after_delay(reminder))
    print(f"Reminder scheduled: '{reminder.message}' in {reminder.delay} seconds")

async def _send_after_delay(reminder: Reminder):
    # delay is now in seconds directly — no conversion needed
    await asyncio.sleep(reminder.delay)
    await send_push(
        message=reminder.message,
        title="Mel Reminder 🤖"
    )
    print(f"Reminder fired: {reminder.message}")