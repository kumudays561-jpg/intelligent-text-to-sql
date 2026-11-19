from rag.retriever import SchemaRetriever
from backend.sql_generator import correct_sql
from backend.sql_validator import validate_sql


question = "Find all customers"

# Retrieve schema
retriever = SchemaRetriever()
result = retriever.retrieve(question)
schema_context = result["schema_context"]

# Deliberately incorrect SQL
incorrect_sql = "SELEC * FROM customers"

print("\nIncorrect SQL:")
print(incorrect_sql)

# Validate the incorrect SQL
is_valid, error_message = validate_sql(incorrect_sql)

print("\nValidation:")
print(error_message)

if not is_valid:

    print("\nSending query to Gemini for correction...")

    corrected_sql = correct_sql(
        question,
        schema_context,
        incorrect_sql,
        error_message
    )

    print("\nCorrected SQL:")
    print(corrected_sql)

    # Validate the corrected query
    corrected_valid, corrected_message = validate_sql(corrected_sql)

    print("\nFinal validation:")
    print(corrected_message)

    if corrected_valid:
        print("\nSELF-CORRECTION SUCCESSFUL!")
    else:
        print("\nCorrection failed.")