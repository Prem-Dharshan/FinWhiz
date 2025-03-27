from abc import ABC, abstractmethod
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

class LanguageModelAdapter(ABC):
    @abstractmethod
    def query(self, prompt: str) -> str:
        pass


class GroqClientAdapter(LanguageModelAdapter):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model

    def query(self, prompt: str) -> str:
        """Query Groq API and return the response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error querying Groq API: {str(e)}"
