from app.models.transaction import Transaction
from datetime import datetime, timezone

def test_transaction_creation():
    transaction = Transaction(
        amount=100.0,
        paid_to="Test Corp",
        event_name="Dinner",
        debit_credit="debit",
        category="Food",
        date=datetime.now(timezone.utc)
    )
    assert transaction.amount == 100.0
    assert transaction.paid_to == "Test Corp"
    