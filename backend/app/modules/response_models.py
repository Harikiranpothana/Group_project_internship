from typing import Any
from pydantic import BaseModel


class QueryResponse(BaseModel):
    success: bool
    question: str
    answer: str
    data: list[dict[str, Any]]