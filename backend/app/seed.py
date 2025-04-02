import os
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.transaction import Transaction
from app.config.database import DBSessionSingleton, Base
from dotenv import load_dotenv
from random import choice, uniform
from datetime import datetime, timedelta, timezone  # Import timezone

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)  # Ensure tables exist

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

    # Use the Singleton DB session
    db_session_instance = DBSessionSingleton()

    # Create a session
    db = db_session_instance()

    try:
        # Get the current date (April 2025) and set bounds for this month
        now = datetime.now(timezone.utc)
        start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        days_in_month = (datetime(now.year, now.month + 1, 1, tzinfo=timezone.utc) - start_of_month).days if now.month < 12 else (datetime(now.year + 1, 1, 1, tzinfo=timezone.utc) - start_of_month).days

        # Generate 500 fake transactions for April 2025
        for _ in range(500):
            # Random date within the current month (April 1st to April 2nd or later as days pass)
            random_days = fake.random_int(min=0, max=min(days_in_month - 1, now.day))  # Up to current day or end of month
            transaction_date = start_of_month + timedelta(days=random_days)

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
        print(f"Successfully seeded 500 transactions into the database for {now.strftime('%B %Y')}.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
        raise  # Re-raise to see full traceback
    finally:
        db.close()  # Close the session directly

if __name__ == "__main__":
    seed_database()
    