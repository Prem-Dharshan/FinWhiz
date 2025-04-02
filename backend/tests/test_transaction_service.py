from app.services.transaction_service import TransactionService
from unittest.mock import MagicMock

def test_get_transactions_empty():
    db_mock = MagicMock()
    db_mock.execute.return_value.fetchall.return_value = []
    service = TransactionService(db_mock)
    result = service.get_transactions("SELECT * FROM transactions")
    assert result == []
    