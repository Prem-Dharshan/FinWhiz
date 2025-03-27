# backend/app/models/transaction.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from app.config.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    paid_to = Column(String, nullable=False)
    event_name = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    debit_credit = Column(String, nullable=False)  # 'debit' or 'credit'
    people = Column(String, nullable=True)  # Who is involved
    who_owes_how_much = Column(Float, nullable=True)  # Amount someone owes
    i_owe_how_much = Column(Float, nullable=True)  # Amount I owe
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)  # Stores transaction date
    