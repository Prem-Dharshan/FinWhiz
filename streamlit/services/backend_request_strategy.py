from abc import ABC, abstractmethod
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class BackendRequestStrategy(ABC):
    @abstractmethod
    def send_request(self, query: str) -> dict:
        pass


class BackendQueryRequest(BackendRequestStrategy):
    def __init__(self):
        self.backend_url = os.getenv("BACKEND_QUERY_URL", "http://backend:8000/query")

    def send_request(self, query: str) -> dict:
        """Send a query to the backend."""
        try:
            response = requests.post(self.backend_url, json={"query": query})
            response.raise_for_status()
            return response.json()  # Returning response as a dictionary
        except requests.exceptions.RequestException as e:
            return {"error": f"Error: {str(e)}"}
