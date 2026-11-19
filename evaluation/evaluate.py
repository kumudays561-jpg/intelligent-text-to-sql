
import csv
import time
import io
from contextlib import redirect_stdout

from backend.pipeline import text_to_sql


test_questions = [
    "List all customers",
    "Find all customers from Bangalore",
    "Find all customers who have placed orders",
    "Find the total quantity of products sold",
    "Find all products that cost more than 5000",
    "List the top 5 selling products",
    "Show the number of products in each category",
    "Display all orders with customer names"
]


results = []

print("\n====================================")
print(" TEXT-TO-SQL FRAMEWORK EVALUATION")
print("====================================")

for index, question in enumerate(test_questions, start=1):

    print(f"\nTest {index}/{len(test_questions)}")
    print("Question:", question)

    start_time = time.perf_counter()

    try:
        # Capture pipeline logs to keep evaluation output readable
        with redirect_stdout(io.StringIO()):
            result = text_to_sql(question)

        response_time = round(
            time.perf_counter() - start_time, 2
        )

        success = result["success"]
        correction = result.get("correction_used", False)

        if success:
            status = "Success"
            print("Status: SUCCESS")
        else:
            status = "Failed"
            print("Status: FAILED")
            print("Error:", result.get("error"))

        print("Relevant tables:", result.get("relevant_tables", []))
        print("Self-correction used:", correction)
        print("Response time:", response_time, "seconds")

        results.append({
            "Question": question,
            "Status": status,
            "Relevant Tables": ", ".join(
                result.get("relevant_tables", [])
            ),
            "Self Correction": correction,
            "Response Time (seconds)": response_time,
            "Error": result.get("error") or ""
        })

    except Exception as error:

        response_time = round(
            time.perf_counter() - start_time, 2
        )

        print("Status: ERROR")
        print("Error:", error)

        results.append({
            "Question": question,
            "Status": "Error",
            "Relevant Tables": "",
            "Self Correction": False,
            "Response Time (seconds)": response_time,
            "Error": str(error)
        })


# Calculate evaluation metrics
total = len(results)

successful = sum(
    1 for item in results if item["Status"] == "Success"
)

failed = total - successful

corrections = sum(
    1 for item in results if item["Self Correction"]
)

average_time = sum(
    item["Response Time (seconds)"] for item in results
) / total

success_rate = (successful / total) * 100

correction_rate = (corrections / total) * 100


# Save evaluation results
with open(
    "evaluation/evaluation_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)


# Display final report
print("\n====================================")
print(" FINAL EVALUATION SUMMARY")
print("====================================")

print("Total test cases:", total)
print("Successful queries:", successful)
print("Failed queries:", failed)

print(f"Execution success rate: {success_rate:.2f}%")
print(f"Self-correction rate: {correction_rate:.2f}%")
print(f"Average response time: {average_time:.2f} seconds")

print("\nDetailed results saved to:")
print("evaluation/evaluation_results.csv")
