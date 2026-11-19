from sqlalchemy import text
from backend.db_connection import engine


def execute_sql(sql):

    try:
        with engine.connect() as connection:

            # Start a read-only transaction
            connection.execute(text("SET TRANSACTION READ ONLY"))

            result = connection.execute(text(sql))

            # Fetch column names
            columns = result.keys()

            # Fetch rows
            rows = result.fetchall()

            return {
                "success": True,
                "columns": list(columns),
                "rows": [list(row) for row in rows],
                "error": None
            }

    except Exception as error:

        return {
            "success": False,
            "columns": [],
            "rows": [],
            "error": str(error)
        }


if __name__ == "__main__":

    query = "SELECT * FROM customers"

    result = execute_sql(query)

    if result["success"]:

        print("\nColumns:")
        print(result["columns"])

        print("\nRows:")

        for row in result["rows"]:
            print(row)

    else:

        print("\nExecution failed:")
        print(result["error"])