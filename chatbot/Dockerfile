# chatbot/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY chatbot/ /app/
COPY .env /app/.env
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]