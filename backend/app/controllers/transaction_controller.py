import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.transaction_service import TransactionService
from app.config.database import SessionLocal
from datetime import datetime

router = APIRouter()

class UserQuery(BaseModel):
    query: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def serialize_datetime(obj):
    """Convert datetime objects to ISO 8601 strings."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

@router.post("/query")
async def query_transactions(user_query: UserQuery, db: Session = Depends(get_db)):
    # Step 1 & 2: Generate SQL query and fetch db_data
    service = TransactionService(db)
    result = service.get_transactions(user_query.query)

    # Check for errors in db_data retrieval
    if "error" in result:
        return result

    # Step 3: Prepare db_data by converting datetime objects to strings
    db_data = [
        {k: serialize_datetime(v) for k, v in row.items()}
        for row in result["db_data"]
    ]
    payload = {
        "query": user_query.query,
        "db_data": db_data
    }
    
    # Send to chatbot service
    chatbot_url = "http://chatbot_service:8002/chat"  # Adjust port if needed
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(chatbot_url, json=payload)
            response.raise_for_status()
            return response.json()  # Step 4: Return chatbot's human-readable response
        except httpx.RequestError as e:
            return {"error": f"Failed to communicate with chatbot service: {str(e)}"}