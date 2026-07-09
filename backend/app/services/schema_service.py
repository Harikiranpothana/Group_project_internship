from typing import Dict, List

from google.cloud import bigquery

from app.services.bigquery_service import bigquery_service
from app.core.config import settings


class SchemaService:
    """
    Retrieves metadata from the configured BigQuery dataset.
    """

    def __init__(self):
        self.client: bigquery.Client = bigquery_service.client

    def get_schema(self) -> Dict:
        """
        Returns the complete schema of the configured dataset.
        """

        schema = {
            "project_id": settings.PROJECT_ID,
            "dataset": settings.DATASET_ID,
            "tables": []
        }

        dataset_ref = self.client.dataset(
            settings.DATASET_ID,
            project=settings.PROJECT_ID
        )

        tables = self.client.list_tables(dataset_ref)

        for table in tables:

            table_ref = self.client.get_table(table.reference)

            table_info = {
                "table_name": table.table_id,
                "columns": []
            }

            for field in table_ref.schema:

                table_info["columns"].append({
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode
                })

            schema["tables"].append(table_info)

        return schema


# Singleton Instance
schema_service = SchemaService()