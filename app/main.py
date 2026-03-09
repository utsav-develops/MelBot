from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.api.routes import chat, health, push, reminder
from app.core.model import load_model
from app.core.agent_model import load_agent_model
from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.scheduler import checkin_scheduler
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    load_agent_model()
    asyncio.create_task(checkin_scheduler())
    yield

app = FastAPI(title="Mel API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:4173",  # Vite dev server
        "http://localhost:3000",  # just in case
        "https://yourdomain.com", # your production frontend
    ],
    allow_credentials=True,  # allows cookies and auth headers
    allow_methods=["*"],     # allows GET, POST, PUT, DELETE, OPTIONS etc
    allow_headers=["*"],     # allows Content-Type, Authorization etc
)

app.include_router(health.router)
app.include_router(chat.router, prefix="/api")
app.include_router(push.router, prefix="/api")
app.include_router(reminder.router, prefix="/api")


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     print("422 validation error:", exc.errors())
#     print("body received:", exc.body)
    
#     return JSONResponse(
#         status_code=422,
#         content={"detail": jsonable_encoder(exc.errors())}  # ← fixes the bytes crash
#     )