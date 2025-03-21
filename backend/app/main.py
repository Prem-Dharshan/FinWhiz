# backend/app/main.py
import time
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import sys
from sqlalchemy import exc

app = FastAPI()

# Conditional import based on execution context
if __name__ == '__main__':
    # Standalone execution (e.g., docker run or python main.py)
    from app.controllers import transaction_controller
    from app.config.database import init_db
else:
    # Package execution (e.g., within Docker Compose or as a module)
    from app.controllers import transaction_controller
    from app.config.database import init_db

app.include_router(transaction_controller.router)
Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def startup_event():
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            init_db()
            print("Database initialized successfully")
            break
        except exc.OperationalError as e:
            retry_count += 1
            print(f"Database connection failed (attempt {retry_count}/{max_retries}): {e}")
            if retry_count == max_retries:
                raise Exception("Failed to connect to database after multiple attempts")
            time.sleep(5)  # Wait 5 seconds before retrying