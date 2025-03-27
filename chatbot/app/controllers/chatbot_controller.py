from fastapi import APIRouter
from app.services.chatbot_service import ChatbotService
from app.services.language_model_adapter import GroqClientAdapter
from pydantic import BaseModel
from dotenv import load_dotenv
import os

router = APIRouter()

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not set in environment")

# Initialize the model adapter and service
model_adapter = GroqClientAdapter(api_key=groq_api_key)
service = ChatbotService(model_adapter)

class ChatQuery(BaseModel):
    query: str
    db_data: list

class SqlQueryRequest(BaseModel):
    query: str

@router.post("/chat")
def chat(chat_query: ChatQuery):
    response = service.query(chat_query.query, chat_query.db_data)
    return {"response": response}

@router.post("/generate_sql")
async def generate_sql(request: SqlQueryRequest):
    sql_query = service.query_sql_generation(request.query)
    return {"sql_query": sql_query}
