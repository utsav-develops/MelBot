from fastapi import APIRouter
from app.schemas.push import PushSubscription
from app.services.push_service import save_subscription, send_push

router = APIRouter()

# frontend calls this when user grants permission
@router.post("/push/subscribe")
async def subscribe(subscription: PushSubscription):
    save_subscription(subscription)
    return {"status": "subscribed"}

# manual trigger for testing
@router.post("/push/test")
async def test_push():
    await send_push("Hey! Whats upp 👋")
    return {"status": "sent"}