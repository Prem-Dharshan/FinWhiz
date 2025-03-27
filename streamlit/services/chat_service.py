from typing import List, Dict
from services.backend_request_strategy import BackendRequestStrategy
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, backend_request_strategy: BackendRequestStrategy):
        self.backend_request_strategy = backend_request_strategy

    def get_response(self, query: str) -> str:
        """Get the bot's response by querying the backend."""
        response_data = self.backend_request_strategy.send_request(query)
        logger.debug(f"Backend response: {response_data}")
        # Extract 'chat_response' from the backend response, with fallback
        return response_data.get("chat_response", "Sorry, I didn't understand that.")
    