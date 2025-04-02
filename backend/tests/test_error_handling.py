from app.services.transaction_service import TransactionService
import pytest
from unittest.mock import MagicMock, patch
import httpx

def test_database_error_handling():
    db_mock = MagicMock()
    db_mock.execute.side_effect = Exception("Database error")
    service = TransactionService(db_mock)
    result = service.get_transactions("SELECT * FROM transactions")
    assert "error" in result
    assert result["error"] == "Error executing query: Database error"

@pytest.mark.asyncio
async def test_service_communication_error():
    db_mock = MagicMock()
    service = TransactionService(db_mock)
    with patch('httpx.AsyncClient.post', side_effect=httpx.RequestError("Mocked error")):
        result = await service.generate_sql_and_execute("SELECT * FROM transactions")
        assert "error" in result
        assert "Failed to communicate with chatbot service" in result["error"]
        