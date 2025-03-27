import json
import logging
from app.services.language_model_adapter import LanguageModelAdapter
from app.config.prompt_template_fetcher import PromptTemplateFetcher

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self, model_adapter: LanguageModelAdapter):
        self.client = model_adapter
        self.prompt_fetcher = PromptTemplateFetcher()

    def fine_tune_prompt_for_sql(self, user_query: str) -> str:
        """Generate the prompt for generating SQL queries."""
        prompt_template = self.prompt_fetcher.fetch("sql_generation")
        return prompt_template.format(query=user_query)

    def clean_sql_query(self, sql_query: str) -> str:
        """Remove markdown code block markers and extra whitespace from SQL query."""
        return sql_query.replace("```sql", "").replace("```", "").strip()

    def query_sql_generation(self, user_query: str) -> str:
        """Generate SQL query by calling language model and clean the output."""
        prompt = self.fine_tune_prompt_for_sql(user_query)
        raw_sql = self.client.query(prompt)
        cleaned_sql = self.clean_sql_query(raw_sql)
        logger.debug(f"Generated SQL: {cleaned_sql}")
        return cleaned_sql

    def fine_tune_prompt(self, user_query: str, db_data: list) -> str:
        """Fine-tune prompt for querying financial data."""
        prompt_template = self.prompt_fetcher.fetch("financial_query")
        return prompt_template.format(query=user_query, db_data=json.dumps(db_data, indent=2))

    def query(self, user_query: str, db_data: list) -> str:
        """Query language model for financial analysis."""
        prompt = self.fine_tune_prompt(user_query, db_data)
        response = self.client.query(prompt)
        logger.debug(f"Chatbot response: {response}")
        return response if response and "Sorry" not in response else "Unable to process query"
    