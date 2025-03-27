from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.transaction_service import TransactionService
from app.config.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class UserQuery(BaseModel):
    query: str

# Factory function to provide TransactionService with a database session
def get_transaction_service(db: Session = Depends(get_db)) -> TransactionService:
    return TransactionService(db)

@router.post("/query")
async def query_transactions(
    user_query: UserQuery,
    service: TransactionService = Depends(get_transaction_service)
):
    # Delegate to the service to process the query
    result = await service.generate_sql_and_execute(user_query.query)
    return result