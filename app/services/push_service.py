import json
import os
from pywebpush import webpush, WebPushException

subscriptions = []

SUBSCRIPTIONS_FILE = "subscriptions.json"

def load_subscriptions() -> list:
    if not os.path.exists(SUBSCRIPTIONS_FILE):
        return []
    with open(SUBSCRIPTIONS_FILE, "r") as f:
        return json.load(f)
    
def save_subscriptions(subscriptions: list):
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(subscriptions, f)


def save_subscription(subscription):
    subscriptions = load_subscriptions()
    # avoid duplicates
    if subscription.endpoint not in [s["endpoint"] for s in subscriptions]:
        subscriptions.append({
            "endpoint": subscription.endpoint,
            "keys": subscription.keys,
        })
        save_subscriptions(subscriptions)
        print(f"Subscription saved: {subscription.endpoint[:50]}...")


async def send_push(message: str, title: str = "Mel 🤖"):
    subscriptions = load_subscriptions()  # ← always load fresh from file
    print(f"Sending to {len(subscriptions)} subscriptions")

    for subscription in subscriptions:
        try:
            print(f"Trying: {subscription['endpoint'][:50]}")
            webpush(
                subscription_info={
                    "endpoint": subscription["endpoint"],
                    "keys": subscription["keys"],
                },
                data=json.dumps({
                    "title": title,
                    "body": message,
                    "icon": "/pwa-192x192.png",
                }),
                vapid_private_key=os.getenv("VAPID_PRIVATE_KEY"),
                vapid_claims={
                    "sub": os.getenv("VAPID_CLAIMS_EMAIL"),
                },
            )
            print("Push sent successfully ✅")
        except WebPushException as e:
            print(f"Push failed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")