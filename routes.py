from fastapi import APIRouter
from pydantic import BaseModel
from chatbot import chatbot_response

router = APIRouter()

# ---------- Models ----------
class ChatRequest(BaseModel):
    message: str
    user_id: str | None = "web"

# ---------- Routes ----------
@router.post("/chat")
def chat(req: ChatRequest):
    reply = chatbot_response(req.message, req.user_id)
    return {"bot_reply": reply}
