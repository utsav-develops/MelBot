import asyncio
from app.schemas.reminder import Reminder
from app.services.push_service import send_push

async def schedule_reminder(reminder: Reminder):
    # fire and forget — don't await, runs in background
    asyncio.create_task(_send_after_delay(reminder))
    print(f"Reminder scheduled: '{reminder.message}' in {reminder.delay} min")

async def _send_after_delay(reminder: Reminder):
    # wait for the specified minutes
    await asyncio.sleep(reminder.delay * 60)
    await send_push(
        message=reminder.message,
        title="Mel Reminder 🤖"
    )
    print(f"Reminder sent: {reminder.message}")