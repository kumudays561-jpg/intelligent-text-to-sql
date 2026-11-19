import sqlglot
from sqlglot import exp


def validate_sql(sql):

    try:
        # Parse SQL using PostgreSQL dialect
        parsed = sqlglot.parse(sql, dialect="postgres")

        # Remove empty statements
        parsed = [statement for statement in parsed if statement]

        if not parsed:
            return False, "Empty SQL query"

        # Only allow one SQL statement
        if len(parsed) > 1:
            return False, "Multiple SQL statements are not allowed"

        statement = parsed[0]

        # Only allow SELECT queries
        if not isinstance(statement, exp.Select):
            return False, "Only SELECT queries are allowed"

        # Dangerous SQL operations
        dangerous_commands = (
            exp.Insert,
            exp.Update,
            exp.Delete,
            exp.Drop,
            exp.Create,
            exp.Alter,
        )

        for command in dangerous_commands:
            if statement.find(command):
                return False, (
                    f"Dangerous SQL operation detected: "
                    f"{command.__name__}"
                )

        return True, "SQL query is valid"

    except Exception as error:
        return False, f"SQL syntax error: {error}"


if __name__ == "__main__":

    test_queries = [
        "SELECT * FROM customers",
        "SELECT SUM(quantity) FROM order_items",
        "DELETE FROM customers",
        "DROP TABLE customers",
        "SELECT * FROM customers; DROP TABLE customers",
        "SELEC * FROM customers"
    ]

    for query in test_queries:

        print("\nQuery:", query)

        is_valid, message = validate_sql(query)

        print("Valid:", is_valid)
        print("Message:", message)