# Allowed SQL Commands
ALLOWED_SQL_COMMANDS = [
    "SELECT",
    "WITH"
]

# Blocked Commands
BLOCKED_SQL_COMMANDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "MERGE",
    "CREATE",
    "REPLACE",
    "GRANT",
    "REVOKE",
    "CALL",
    "EXECUTE"
]

# Blocked Patterns
BLOCKED_PATTERNS = [
    "SELECT *",
    ";",
    "--",
    "/*",
    "*/",
    "XP_",
    "INFORMATION_SCHEMA"
]

# Required Keywords
REQUIRED_KEYWORDS = [
    "SELECT",
    "FROM"
]

# Limits
MAX_QUERY_LENGTH = 5000
DEFAULT_LIMIT = 100
REQUIRE_LIMIT = True