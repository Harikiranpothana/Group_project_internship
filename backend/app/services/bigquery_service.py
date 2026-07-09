from typing import List, Dict, Any

from google.cloud import bigquery

from app.core.config import settings


class BigQueryService:
    """
    Handles all communication with Google BigQuery.
    """

    def __init__(self):

        self.client = bigquery.Client.from_service_account_json(
            settings.GOOGLE_APPLICATION_CREDENTIALS,
            project=settings.PROJECT_ID
        )

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """
        Executes a SQL query and returns the result
        as a list of dictionaries.
        """

        query_job = self.client.query(sql)

        results = query_job.result()

        return [dict(row.items()) for row in results]


# Singleton instance
bigquery_service = BigQueryService()