from typing import Any

from pydantic import BaseModel


class QueryResponse(BaseModel):
    """
    Standard response returned by the InsightIQ API.
    """

    success: bool
    message: str

    # AI-generated business explanation.
    # Empty for now; we'll populate it later.
    answer: str | None = None

    # Raw query results from BigQuery.
    data: list[dict[str, Any]]

    # Number of records returned.
    row_count: int