from google import genai

from app.core.config import settings


class ExplanationService:
    """
    Uses Gemini to explain SQL query results in
    simple business language.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate_explanation(
        self,
        question: str,
        sql: str,
        data: list
    ) -> str:

        preview = data[:10]

        prompt = f"""
You are a Senior Business Intelligence Analyst.

The user asked:

{question}

SQL executed:

{sql}

Query Result:

{preview}

Write a short business explanation.

Rules:
- Maximum 120 words.
- Don't mention SQL.
- Explain the result in simple English.
- Mention interesting observations if present.
- If there are no rows, clearly state that no records matched.

Return only the explanation.
"""

        response = self.client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()


explanation_service = ExplanationService()