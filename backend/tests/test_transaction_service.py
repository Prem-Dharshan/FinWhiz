# tests/test_transaction_service.py

from unittest.mock import MagicMock

from app.services.transaction_service import TransactionService

def test_get_transactions():
    db_mock = MagicMock()
    db_mock.execute.return_value.mappings.return_value = [{'id': 1, 'amount': 100}]
    service = TransactionService(db_mock)
    
    result = service.get_transactions("SELECT * FROM transactions")
    
    assert "db_data" in result
    assert len(result["db_data"]) == 1
    assert result["db_data"][0]["id"] == 1
