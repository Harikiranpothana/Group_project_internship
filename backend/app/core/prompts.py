def build_sql_prompt(schema: dict, question: str) -> str:
    """
    Builds the prompt for Gemini to generate Google BigQuery SQL.
    """

    schema_text = ""

    for table in schema["tables"]:

        schema_text += (
            f"\nTable: {table['table_name']}\n"
            f"Full Name: `{table['full_table_name']}`\n"
        )

        for column in table["columns"]:

            schema_text += (
                f"  - {column['name']} "
                f"({column['type']})\n"
            )

    prompt = f"""
You are an expert Google BigQuery SQL developer.

Generate ONLY a valid Google BigQuery SQL query.

=========================
DATABASE SCHEMA
=========================

{schema_text}

=========================
IMPORTANT RULES
=========================

1. Return ONLY SQL.
2. Never explain anything.
3. Never use markdown.
4. Never use ```sql.
5. Never use SELECT *.
6. Select only the required columns.
7. Use ONLY the tables and columns listed above.
8. NEVER invent tables or columns.
9. NEVER modify data.
10. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE or MERGE.
11. Always include LIMIT 100 unless the user requests an aggregate.
12. If a JOIN is required, infer it using common key names.
13. The SQL must execute directly in Google BigQuery.
14. ALWAYS use the FULLY QUALIFIED table name exactly as shown.
15. Never write:

FROM dimpassenger

Instead ALWAYS write:

FROM `cablytics.cabwarehouse.dimpassenger`

16. Every FROM and JOIN must use the FULLY QUALIFIED table name.

=========================
USER QUESTION
=========================

{question}

Return ONLY the SQL query.
"""

    return prompt.strip()