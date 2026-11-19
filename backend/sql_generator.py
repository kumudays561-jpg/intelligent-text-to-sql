from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def generate_sql(question, schema_context):

    schema_text = ""

    for table_name, details in schema_context.items():

        schema_text += f"\nTable: {table_name}\n"

        schema_text += "Columns:\n"

        for column in details["columns"]:
            schema_text += (
                f"- {column['name']} ({column['type']})\n"
            )

        schema_text += f"Primary Key: {details['primary_key']}\n"

        schema_text += "Foreign Keys:\n"

        for fk in details["foreign_keys"]:
            schema_text += (
                f"- {fk['column']} references "
                f"{fk['references_table']} "
                f"{fk['references_column']}\n"
            )

    prompt = f"""
You are an expert PostgreSQL SQL query generator.

Your task is to convert the user's natural language question
into a correct PostgreSQL SQL query.

Use ONLY the tables and columns provided in the schema.

Rules:
1. Generate only SQL.
2. Do not explain the query.
3. Do not use markdown code blocks.
4. Do not invent tables or columns.
5. Use appropriate JOINs when required.
6. Use PostgreSQL syntax.
7. If aggregation is required, use appropriate aggregate functions.
8. If the question cannot be answered using the schema,
   return: CANNOT_GENERATE_SQL

Database Schema:
{schema_text}

User Question:
{question}

SQL Query:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    sql = response.text.strip()

    # Remove markdown code blocks if the LLM accidentally returns them
    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

    return sql

def correct_sql(question, schema_context, incorrect_sql, error_message):

    schema_text = ""

    for table_name, details in schema_context.items():

        schema_text += f"\nTable: {table_name}\nColumns:\n"

        for column in details["columns"]:
            schema_text += f"- {column['name']} ({column['type']})\n"

        schema_text += f"Primary Key: {details['primary_key']}\n"

        schema_text += "Foreign Keys:\n"

        for fk in details["foreign_keys"]:
            schema_text += (
                f"- {fk['column']} references "
                f"{fk['references_table']} "
                f"{fk['references_column']}\n"
            )

    prompt = f"""
You are an expert PostgreSQL SQL debugger.

Correct the SQL query based on the error.

Rules:
1. Return only the corrected SQL.
2. Do not include explanations.
3. Do not use markdown code blocks.
4. Only use tables and columns in the provided schema.
5. Only generate SELECT queries.

Database Schema:
{schema_text}

User Question:
{question}

Incorrect SQL:
{incorrect_sql}

Error:
{error_message}

Corrected SQL:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    corrected_sql = response.text.strip()

    if corrected_sql.startswith("```"):
        corrected_sql = corrected_sql.replace("```sql", "")
        corrected_sql = corrected_sql.replace("```", "")
        corrected_sql = corrected_sql.strip()

    return corrected_sql


if __name__ == "__main__":

    sample_schema = {
        "customers": {
            "columns": [
                {"name": "customer_id", "type": "INTEGER"},
                {"name": "name", "type": "VARCHAR"},
                {"name": "city", "type": "VARCHAR"}
            ],
            "primary_key": ["customer_id"],
            "foreign_keys": []
        }
    }

    question = "Find all customers from Bangalore"

    result = generate_sql(question, sample_schema)

    print("\nGenerated SQL:")
    print(result)