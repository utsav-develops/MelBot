from pydantic import BaseModel

class Reminder(BaseModel):
    message: str
    delay:   int