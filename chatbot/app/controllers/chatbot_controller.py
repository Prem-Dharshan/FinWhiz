from fastapi import APIRouter
from app.services.chatbot_service import ChatbotService
from pydantic import BaseModel

router = APIRouter()
service = ChatbotService()

class ChatQuery(BaseModel):
    query: str
    db_data: list

@router.post("/chat")
def chat(chat_query: ChatQuery):
    response = service.query(chat_query.query, chat_query.db_data)
    return {"response": response}