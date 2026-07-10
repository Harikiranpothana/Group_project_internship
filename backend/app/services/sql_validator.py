import re

from app.services.schema_service import schema_service


class SQLValidator:
    """
    Validates AI-generated SQL before execution.
    """

    def validate(self, sql: str):

        sql = sql.strip()

        self._check_empty(sql)
        self._check_single_statement(sql)
        self._check_select(sql)
        self._check_forbidden_keywords(sql)
        self._check_select_star(sql)
        self._check_limit(sql)
        self._check_comments(sql)
        self._check_tables(sql)

        return sql

    # -------------------------------------------------------

    def _check_empty(self, sql):

        if not sql:
            raise ValueError("Generated SQL is empty.")

    # -------------------------------------------------------

    def _check_single_statement(self, sql):

        sql = sql.rstrip(";")

        if ";" in sql:
            raise ValueError(
                "Multiple SQL statements are not allowed."
            )

    # -------------------------------------------------------

    def _check_select(self, sql):

        if not sql.upper().startswith("SELECT"):
            raise ValueError(
                "Only SELECT statements are allowed."
            )

    # -------------------------------------------------------

    def _check_forbidden_keywords(self, sql):

        forbidden = [
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
            "ALTER",
            "CREATE",
            "MERGE",
            "TRUNCATE",
            "CALL",
            "EXECUTE",
            "GRANT",
            "REVOKE"
        ]

        upper = sql.upper()

        for keyword in forbidden:

            if keyword in upper:
                raise ValueError(
                    f"{keyword} statements are forbidden."
                )

    # -------------------------------------------------------

    def _check_select_star(self, sql):

        if re.search(
            r"SELECT\s+\*",
            sql,
            re.IGNORECASE
        ):

            raise ValueError(
                "SELECT * is not allowed."
            )

    # -------------------------------------------------------

    def _check_limit(self, sql):

        match = re.search(
            r"LIMIT\s+(\d+)",
            sql,
            re.IGNORECASE
        )

        if match is None:
            raise ValueError(
                "LIMIT clause is required."
            )

        limit = int(match.group(1))

        if limit > 100:
            raise ValueError(
                "LIMIT cannot exceed 100."
            )

    # -------------------------------------------------------

    def _check_comments(self, sql):

        if "--" in sql or "/*" in sql:

            raise ValueError(
                "SQL comments are not allowed."
            )

    # -------------------------------------------------------

    def _check_tables(self, sql):

        schema = schema_service.get_schema()

        allowed_tables = [
            table["table_name"].lower()
            for table in schema["tables"]
        ]

        # Extract tables after FROM or JOIN
        matches = re.findall(
            r"(?:FROM|JOIN)\s+`?([A-Za-z0-9_.]+)`?",
            sql,
            re.IGNORECASE
        )

        print("\nAllowed Tables:", allowed_tables)
        print("Matched Tables:", matches)

        for table in matches:

            # Handle project.dataset.table
            table_name = table.split(".")[-1].lower()

            print("Checking:", table_name)

            if table_name not in allowed_tables:

                raise ValueError(
                    f"Unknown table '{table_name}'."
                )


# Singleton Instance
sql_validator = SQLValidator()