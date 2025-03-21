import json
import logging
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

MODEL = "llama-3.3-70b-versatile"

class ChatbotService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def fine_tune_prompt(self, user_query: str, db_data: list) -> str:
        logger.debug("Generating fine-tuned prompt for Groq")
        prompt = f"""
        You are an AI model trained to assist with financial analysis. The user query is: "{user_query}".
        The relevant transaction data from the local database is as follows:
        {json.dumps(db_data, indent=2)}
        Provide a clear and concise response based on the user's query and the provided data.
        """
        logger.debug("Prompt generated")
        return prompt

    def query(self, user_query: str, db_data: list) -> str:
        logger.debug(f"Querying Groq API for user query: {user_query}")
        prompt = self.fine_tune_prompt(user_query, db_data)
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            groq_response = response.choices[0].message.content.strip()
            logger.debug(f"Grok API response: {groq_response}")
            return groq_response
        except Exception as e:
            logger.error(f"Error querying Groq API: {str(e)}")
            return f"Error querying Groq API: {str(e)}"
        