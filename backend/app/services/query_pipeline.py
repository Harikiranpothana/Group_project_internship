import re

from app.services.schema_service import schema_service
from app.services.gemini_service import gemini_service
from app.services.sql_validator import sql_validator
from app.services.bigquery_service import bigquery_service


class QueryPipeline:
    """
    Complete Natural Language → SQL → BigQuery pipeline.
    """

    # --------------------------------------------------
    # Automatically qualify table names
    # --------------------------------------------------

    def qualify_table_names(self, sql: str, schema: dict) -> str:
        """
        Converts:

            FROM dimpassenger

        into

            FROM `project.dataset.dimpassenger`

        and likewise for JOIN statements.
        """

        for table in schema["tables"]:

            table_name = table["table_name"]
            full_table = f"`{table['full_table_name']}`"

            # Replace FROM table
            sql = re.sub(
                rf"\bFROM\s+`?{table_name}`?\b",
                f"FROM {full_table}",
                sql,
                flags=re.IGNORECASE
            )

            # Replace JOIN table
            sql = re.sub(
                rf"\bJOIN\s+`?{table_name}`?\b",
                f"JOIN {full_table}",
                sql,
                flags=re.IGNORECASE
            )

        return sql

    # --------------------------------------------------
    # Main Pipeline
    # --------------------------------------------------

    def process_query(self, question: str):

        try:

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

            print("\n============= GENERATED SQL =============")
            print(generated_sql)
            print("=========================================\n")

            # ------------------------------------
            # Step 3 : Validate SQL
            # ------------------------------------

            validated_sql = sql_validator.validate(
                generated_sql
            )

            # ------------------------------------
            # Step 4 : Qualify Table Names
            # ------------------------------------

            qualified_sql = self.qualify_table_names(
                validated_sql,
                schema
            )

            print("\n============= QUALIFIED SQL =============")
            print(qualified_sql)
            print("=========================================\n")

            # ------------------------------------
            # Step 5 : Execute SQL
            # ------------------------------------

            results = bigquery_service.execute_query(
                qualified_sql
            )

            # ------------------------------------
            # Step 6 : Return Response
            # ------------------------------------

            return {
                "success": True,
                "message": "Query executed successfully.",
                "answer": None,
                "data": results,
                "row_count": len(results)
            }

        except Exception as e:

            print("\n============= PIPELINE ERROR ============")
            print(str(e))
            print("=========================================\n")

            raise Exception(str(e))


# Singleton Instance
query_pipeline = QueryPipeline()