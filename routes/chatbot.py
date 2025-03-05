from fastapi import APIRouter
from pydantic import BaseModel
from services.chatbot_service import handle_user_message

router = APIRouter()

class Message(BaseModel):
    user_id: int
    message: str

@router.post("/chat/")
async def chat_with_bot(message: Message):
    response = await handle_user_message(message.user_id, message.message)
    return {"response": response}
