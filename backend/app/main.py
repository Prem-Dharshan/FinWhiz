import time
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.controllers import transaction_controller
from app.config.database import get_db, db_session_instance
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text


app = FastAPI(title="FinWhiz Backend")

app.include_router(transaction_controller.router)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.on_event("startup")
async def startup_event():
    """Initialize the database with retry logic on startup."""
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Use a session to test connectivity and initialize schema
            db = next(get_db())
            db.execute(text("SELECT 1"))
            print("Database connection established and schema initialized successfully")
            break
        except SQLAlchemyError as e:  # Specific exception for SQLAlchemy issues
            retry_count += 1
            print(f"Database connection failed (attempt {retry_count}/{max_retries}): {e}")
            if retry_count == max_retries:
                raise RuntimeError("Failed to connect to database after multiple attempts") from e
            time.sleep(5)  # Wait 5 seconds before retrying
        finally:
            if 'db' in locals():
                db.close()  # Ensure session is closed even on failure
