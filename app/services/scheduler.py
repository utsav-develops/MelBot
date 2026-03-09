import asyncio
import random
from app.services.push_service import send_push
from app.core.model import generate

# fun check-in prompts Mel picks from
CHECKIN_PROMPTS = [
    "Generate a short, fun, random check-in message as Mel the AI bot. Max 1 sentence.",
    "Generate a witty reminder to take a break. Max 1 sentence. Sign off as Mel.",
    "Generate a motivational message. Keep it short and fun. Sign off as Mel.",
]

async def checkin_scheduler():
    while True:
        # wait random time between 1-3 hours
        wait_seconds = random.randint(3600, 10800)
        await asyncio.sleep(wait_seconds)

        # generate AI message
        prompt = random.choice(CHECKIN_PROMPTS)
        message = generate(prompt)

        await send_push(message, title="Mel is thinking of you 🤖")
        print(f"Check-in sent: {message}")