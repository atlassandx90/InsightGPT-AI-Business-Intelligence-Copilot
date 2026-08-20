FORBIDDEN = [
    "DROP",
    "DELETE",
    "TRUNCATE",
    "ALTER",
    "UPDATE",
    "INSERT"
]


def validate_sql(sql: str):

    upper_sql = sql.upper()

    for keyword in FORBIDDEN:
        if keyword in upper_sql:
            return False

    return True