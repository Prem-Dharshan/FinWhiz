import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from groq import Groq
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY not found in .env file")
    raise ValueError("GROQ_API_KEY not found in .env file")
logger.info("GROQ_API_KEY loaded successfully")
client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def generate_sql_query(self, user_query: str) -> str:
        logger.debug(f"Generating SQL query for user query: {user_query}")
        prompt = f"""
        You are a SQL expert for PostgreSQL. Given the following table schema for 'transactions':
        - id INTEGER PRIMARY KEY AUTOINCREMENT
        - amount REAL NOT NULL
        - paid_to TEXT NOT NULL
        - event_name TEXT
        - notes TEXT
        - debit_credit TEXT (debit or credit) NOT NULL
        - people TEXT
        - who_owes_how_much REAL
        - i_owe_how_much REAL
        - category TEXT NOT NULL
        - date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        Generate a sharp, precise SQL query to fetch relevant data for the following user query:
        "{user_query}"

        - Use PostgreSQL syntax only (e.g., use DATE_TRUNC('month', CURRENT_TIMESTAMP) or CURRENT_DATE - INTERVAL '1 month' for date operations).
        - Always include relevant fields based on the user query and ensure group by/analytical queries are well understood.
        - Keep it minimal and focused: only include conditions directly relevant to the query.
        - Avoid unnecessary filters (e.g., don’t assume specific values like 'YOUR_NAME' unless explicitly stated).
        - Return only the SQL query as plain text, no explanations.
        """
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.5
            )
            sql_query = response.choices[0].message.content.strip()
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            logger.debug(f"Generated SQL query: {sql_query}")
            return sql_query
        except Exception as e:
            logger.error(f"Failed to generate SQL query: {str(e)}")
            fallback_query = f"SELECT * FROM transactions LIMIT 1 -- Error: {str(e)}"
            logger.debug(f"Returning fallback SQL query: {fallback_query}")
            return fallback_query

    def get_transactions(self, user_query: str):
        logger.debug(f"Processing user query: {user_query}")
        sql_query = self.generate_sql_query(user_query)
        logger.debug(f"Executing SQL query: {sql_query}")
        try:
            result = self.db.execute(text(sql_query))
            rows = [dict(row) for row in result.mappings()]
            logger.debug(f"Query executed successfully, fetched {len(rows)} rows")
            return {"db_data": rows}
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return {"error": f"Error executing query: {str(e)}"}