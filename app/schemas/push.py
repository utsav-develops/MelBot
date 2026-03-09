from pydantic import BaseModel

class PushSubscription(BaseModel):
    endpoint: str
    keys: dict 