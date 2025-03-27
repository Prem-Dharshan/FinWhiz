# tests/test_transaction.py

from app.services.transaction_service import TransactionService
from app.main import app
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_service():
    with patch.object(TransactionService, 'generate_sql_and_execute', return_value={"query": "SELECT * FROM transactions", "db_data": []}):
        yield

def test_query_transactions(mock_service):
    # Test the /query endpoint
    response = client.post("/query", json={"query": "SELECT * FROM transactions"})
    assert response.status_code == 200
    assert "query" in response.json()
    assert "db_data" in response.json()
