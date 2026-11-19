import json

SCHEMA_PATH = "datasets/schema.json"


def load_schema():
    with open(SCHEMA_PATH, "r") as file:
        return json.load(file)


def create_schema_documents():

    schema = load_schema()

    documents = []

    for table_name, details in schema.items():

        columns = []

        for column in details["columns"]:
            columns.append(f"{column['name']} ({column['type']})")

        primary_keys = details["primary_key"]
        foreign_keys = details["foreign_keys"]

        document = f"""
Table: {table_name}
Columns: {', '.join(columns)}
Primary Keys: {', '.join(primary_keys)}
Foreign Key Relationships:
"""

        if foreign_keys:

            for fk in foreign_keys:

                document += (
                    f"\n{', '.join(fk['column'])} references "
                    f"{fk['references_table']}."
                    f"{', '.join(fk['references_column'])}"
                )

        else:
            document += " No foreign keys."

        documents.append({
            "table": table_name,
            "content": document.strip()
        })

    return documents


if __name__ == "__main__":

    docs = create_schema_documents()

    for doc in docs:
        print("\n" + "=" * 50)
        print(doc["content"])