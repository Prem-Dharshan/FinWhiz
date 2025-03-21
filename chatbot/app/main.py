from app.controllers import chatbot_controller
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.include_router(chatbot_controller.router)

Instrumentator().instrument(app).expose(app)