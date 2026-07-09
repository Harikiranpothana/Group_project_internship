def build_sql_prompt(schema: dict, question: str) -> str:
    """
    Builds the prompt for Gemini to generate SQL.
    """

    schema_text = ""

    for table in schema["tables"]:

        schema_text += f"\nTable: {table['table_name']}\n"

        for column in table["columns"]:
            schema_text += (
                f"  - {column['name']} "
                f"({column['type']})\n"
            )

    prompt = f"""
You are an expert Google BigQuery SQL developer.

Your task is to generate ONLY a valid Google BigQuery SQL query.

DATABASE SCHEMA
----------------
{schema_text}

RULES
----------------
1. Generate ONLY SQL.
2. Do NOT explain anything.
3. Do NOT use markdown.
4. Do NOT use ```sql.
5. Never use SELECT *.
6. Select only required columns.
7. Use only tables and columns provided in the schema.
8. Never create or modify data.
9. Never use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE or MERGE.
10. Prefer LIMIT 100 unless the question asks for aggregates.
11. If a JOIN is required, infer it using common key names.
12. Output must be executable in Google BigQuery.

USER QUESTION
----------------
{question}

Return ONLY the SQL query.
"""

    return prompt.strip()