from app.services.schema_service import schema_service
from app.services.gemini_service import gemini_service
from app.services.sql_validator import sql_validator
from app.services.bigquery_service import bigquery_service


class QueryPipeline:
    """
    Complete Natural Language -> SQL -> BigQuery pipeline.
    """

    def process_query(self, question: str):

        # -----------------------------
        # Step 1 : Load Schema
        # -----------------------------

        schema = schema_service.get_schema()

        # -----------------------------
        # Step 2 : Generate SQL
        # -----------------------------

        generated_sql = gemini_service.generate_sql(
            schema,
            question
        )

        # -----------------------------
        # Step 3 : Validate SQL
        # -----------------------------

        validated_sql = sql_validator.validate(
            generated_sql
        )

        # -----------------------------
        # Step 4 : Execute SQL
        # -----------------------------

        results = bigquery_service.execute_query(
            validated_sql
        )

        # -----------------------------
        # Step 5 : Return Raw Data
        # -----------------------------

        return {
            "success": True,
            "data": results
        }


# Singleton Instance
query_pipeline = QueryPipeline()