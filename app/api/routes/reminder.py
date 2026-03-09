# app/api/routes/reminder.py
from fastapi import APIRouter
from app.schemas.reminder import Reminder
from app.services.reminder_service import schedule_reminder

router = APIRouter()

@router.post("/reminder")
async def set_reminder(reminder: Reminder):
    await schedule_reminder(reminder)
    return {"status": "reminder set", "in_minutes": reminder.delay}