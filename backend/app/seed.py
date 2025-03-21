import os
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.transaction import Transaction
from app.config.database import Base
from dotenv import load_dotenv
from random import choice, uniform
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Faker
fake = Faker()

# Categories for transactions
CATEGORIES = [
    "Food", "Entertainment", "Transportation", "Utilities", "Shopping",
    "Healthcare", "Travel", "Rent", "Groceries", "Miscellaneous"
]

# Function to seed the database
def seed_database():
    # Create the tables if they don't exist
    Base.metadata.drop_all(bind=engine)  # Clear existing data
    Base.metadata.create_all(bind=engine)

    # Create a session
    db = SessionLocal()

    try:
        # Generate 500 fake transactions
        for _ in range(500):
            # Random date within the last 30 days
            random_days = fake.random_int(min=0, max=30)
            transaction_date = datetime.utcnow() - timedelta(days=random_days)

            # Random amount between 1.00 and 1000.00
            amount = round(uniform(1.0, 1000.0), 2)

            # Random debit or credit
            debit_credit = choice(["debit", "credit"])

            # Random people involved (sometimes null)
            people = fake.name() if fake.random_int(min=0, max=1) == 1 else None

            # Random debt/owe amounts (sometimes null)
            who_owes = round(uniform(0.0, amount), 2) if fake.random_int(min=0, max=1) == 1 else None
            i_owe = round(uniform(0.0, amount), 2) if fake.random_int(min=0, max=1) == 1 else None

            # Create a transaction
            transaction = Transaction(
                amount=amount,
                paid_to=fake.company(),  # Always present
                event_name=fake.word(),  # Always present
                notes=fake.sentence() if fake.random_int(min=0, max=1) == 1 else None,  # Optional
                debit_credit=debit_credit,
                people=people,
                who_owes_how_much=who_owes,
                i_owe_how_much=i_owe,
                category=choice(CATEGORIES),  # Always present
                date=transaction_date
            )
            db.add(transaction)

        # Commit the transactions to the database
        db.commit()
        print("Successfully seeded 500 transactions into the database.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()