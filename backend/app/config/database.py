from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import threading
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/db_name")

# Define Base here to avoid circular imports
Base = declarative_base()

class DBSessionSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                # Create the engine and session factory
                engine = create_engine(DATABASE_URL)
                cls._instance = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                # Initialize schema (metadata) here; no need to import Transaction yet
                Base.metadata.create_all(bind=engine)
        return cls._instance

    def close(self, db: Session):
        """Close the session properly."""
        db.close()

# Instantiate the singleton
db_session_instance = DBSessionSingleton()

# Dependency injection function
def get_db() -> Session:
    db = db_session_instance()
    try:
        yield db
    finally:
        # db_session_instance.close(db)
        db.close()

