from typing import Dict
from google.cloud import bigquery

from app.services.bigquery_service import bigquery_service
from app.core.config import settings


class SchemaService:
    """
    Retrieves and caches metadata from the configured BigQuery dataset.
    """

    def __init__(self):
        # Reuse the existing BigQuery client
        self.client: bigquery.Client = bigquery_service.client

        # Cache schema after first load
        self._schema_cache = None

    def get_schema(self) -> Dict:
        """
        Returns the complete schema of the configured dataset.

        The schema is cached after the first retrieval to avoid
        repeated API calls to BigQuery.
        """

        # Return cached schema if already loaded
        if self._schema_cache is not None:
            return self._schema_cache

        schema = {
            "project_id": settings.PROJECT_ID,
            "dataset": settings.DATASET_ID,
            "tables": []
        }

        try:

            dataset_ref = self.client.dataset(
                settings.DATASET_ID,
                project=settings.PROJECT_ID
            )

            tables = self.client.list_tables(dataset_ref)

            for table in tables:

                table_ref = self.client.get_table(table.reference)

                table_info = {
                    "table_name": table.table_id,
                    "full_table_name": (
                        f"{settings.PROJECT_ID}."
                        f"{settings.DATASET_ID}."
                        f"{table.table_id}"
                    ),
                    "columns": []
                }

                for field in table_ref.schema:

                    table_info["columns"].append({
                        "name": field.name,
                        "type": field.field_type,
                        "mode": field.mode
                    })

                schema["tables"].append(table_info)

            # Store schema in cache
            self._schema_cache = schema

            return self._schema_cache

        except Exception as e:
            raise Exception(f"Failed to retrieve schema: {e}")


# Singleton Instance
schema_service = SchemaService()