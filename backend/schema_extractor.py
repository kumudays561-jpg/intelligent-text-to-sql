
from sqlalchemy import inspect
from backend.db_connection import engine
import json


def extract_schema():

    inspector = inspect(engine)

    schema = {}

    tables = inspector.get_table_names()

    for table in tables:

        columns = inspector.get_columns(table)

        primary_keys = inspector.get_pk_constraint(table)

        foreign_keys = inspector.get_foreign_keys(table)

        column_details = []

        for column in columns:

            column_details.append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"]
            })

        foreign_key_details = []

        for fk in foreign_keys:

            foreign_key_details.append({
                "column": fk["constrained_columns"],
                "references_table": fk["referred_table"],
                "references_column": fk["referred_columns"]
            })

        schema[table] = {
            "columns": column_details,
            "primary_key": primary_keys.get(
                "constrained_columns", []
            ),
            "foreign_keys": foreign_key_details
        }

    return schema


if __name__ == "__main__":

    database_schema = extract_schema()

    print(json.dumps(
        database_schema,
        indent=4
    ))

    with open("datasets/schema.json", "w") as file:
        json.dump(database_schema, file, indent=4)

    print("\nSchema extracted successfully!")
