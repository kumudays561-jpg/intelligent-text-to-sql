
from rag.retriever import SchemaRetriever
from backend.sql_generator import generate_sql, correct_sql
from backend.sql_validator import validate_sql
from backend.sql_executor import execute_sql


def text_to_sql(question):

    print("\nUser Question:", question)

    print("\nRetrieving relevant schema...")

    retriever = SchemaRetriever()
    retrieval_result = retriever.retrieve(question)

    schema_context = retrieval_result["schema_context"]
    relevant_tables = retrieval_result["relevant_tables"]

    print("\nRelevant Tables:")
    print(relevant_tables)

    print("\nGenerating SQL using Gemini...")

    sql = generate_sql(question, schema_context)

    max_attempts = 3
    correction_used = False

    for attempt in range(max_attempts):

        print(f"\n--- Attempt {attempt + 1} ---")

        print("\nGenerated SQL:")
        print(sql)

        print("\nValidating SQL...")

        is_valid, validation_message = validate_sql(sql)

        print(validation_message)

        if not is_valid:

            error_message = validation_message

        else:

            print("\nExecuting SQL...")

            execution_result = execute_sql(sql)

            if execution_result["success"]:

                print("\nQuery executed successfully!")

                print("\nColumns:")
                print(execution_result["columns"])

                print("\nResults:")

                for row in execution_result["rows"]:
                    print(row)

                return {
                    "success": True,
                    "sql": sql,
                    "columns": execution_result["columns"],
                    "rows": execution_result["rows"],
                    "relevant_tables": relevant_tables,
                    "correction_used": correction_used,
                    "error": None
                }

            else:

                error_message = execution_result["error"]

                print("\nExecution Error:")
                print(error_message)

        if attempt < max_attempts - 1:

            print("\nAttempting self-correction...")

            correction_used = True

            sql = correct_sql(
                question,
                schema_context,
                sql,
                error_message
            )

        else:

            print("\nMaximum attempts reached.")

            return {
                "success": False,
                "sql": sql,
                "columns": [],
                "rows": [],
                "relevant_tables": relevant_tables,
                "correction_used": correction_used,
                "error": error_message
            }


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    result = text_to_sql(question)
