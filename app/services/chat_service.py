from app.core.model import generate
from app.schemas.chat import Message, ChatRequest, ChatResponse, UsageInfo, ChatMessage

def handle_chat(request: ChatRequest) -> ChatResponse:
    # Build history
    print("received:", request)
    history = [{"role": m.role, "content": m.content} for m in request.history]
    history.append({"role": "user", "content": request.message})

    # Get reply from Mel
    reply = generate(history)

    # Update history
    history.append({"role": "assistant", "content": reply})

    print("reply generated", reply)

    return ChatResponse(
        message=ChatMessage(
            role="assistant",
            content=reply
        ),
        usage=UsageInfo(
            promptTokens=0,
            completionTokens=0,
            totalTokens=0,
        )
    )  