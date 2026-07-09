from google import genai

from app.core.config import settings
from app.core.prompts import build_sql_prompt


class GeminiService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate_sql(self, schema: dict, question: str) -> str:

        prompt = build_sql_prompt(schema, question)

        response = self.client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=prompt
        )

        sql = response.text.strip()

        return sql


# Singleton Instance
gemini_service = GeminiService()