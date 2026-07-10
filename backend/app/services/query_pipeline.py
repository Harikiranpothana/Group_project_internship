from app.services.schema_service import schema_service
from app.services.gemini_service import gemini_service
from app.services.sql_validator import sql_validator
from app.services.bigquery_service import bigquery_service


class QueryPipeline:
    """
    Complete Natural Language -> SQL -> BigQuery pipeline.
    """

    def process_query(self, question: str):
        """
        Executes the complete pipeline:
        1. Retrieve schema
        2. Generate SQL using Gemini
        3. Validate SQL
        4. Execute SQL on BigQuery
        5. Return results
        """

        # ------------------------------------
        # Step 1 : Retrieve Schema
        # ------------------------------------
        schema = schema_service.get_schema()

        # ------------------------------------
        # Step 2 : Generate SQL
        # ------------------------------------
        generated_sql = gemini_service.generate_sql(
            schema=schema,
            question=question
        )

        # ------------------------------------
        # Step 3 : Validate SQL
        # ------------------------------------
        validated_sql = sql_validator.validate(
            generated_sql
        )

        # ------------------------------------
        # Step 4 : Execute Query
        # ------------------------------------
        results = bigquery_service.execute_query(
            validated_sql
        )

        # ------------------------------------
        # Step 5 : Return Response
        # ------------------------------------
        return {
            "success": True,
            "message": "Query executed successfully.",
            "answer": None,          # Will be added after Explanation Service
            "data": results,
            "row_count": len(results)
        }


# Singleton Instance
query_pipeline = QueryPipeline()