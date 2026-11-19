
import streamlit as st
import pandas as pd

from backend.pipeline import text_to_sql

st.set_page_config(
    page_title="Intelligent Text-to-SQL",
    page_icon="🧠",
    layout="wide"
)

# Application heading
st.title("🧠 Intelligent Text-to-SQL Framework")

st.markdown(
    "Convert natural language questions into SQL queries "
    "using Retrieval-Augmented Generation and Gemini."
)

st.divider()

# User input
st.subheader("Ask your database")

question = st.text_area(
    "Enter your question in plain English:",
    placeholder="Example: Find all customers from Bangalore",
    height=100
)

if st.button("Generate SQL", type="primary"):

    if question.strip():

        with st.spinner("Processing your question..."):

            try:
                result = text_to_sql(question)

                # Display retrieved schema
                st.subheader("RAG Schema Retrieval")

                tables = result.get("relevant_tables", [])

                if tables:
                    st.success("Relevant tables retrieved successfully")

                    st.write("Tables used:")
                    st.write(", ".join(tables))

                # Display SQL
                st.subheader("Generated SQL Query")

                st.code(
                    result["sql"],
                    language="sql"
                )

                # Display correction status
                st.subheader("Self-Correction Status")

                if result.get("correction_used", False):
                    st.info(
                        "Self-correction was triggered "
                        "to fix an SQL issue."
                    )
                else:
                    st.success(
                        "No self-correction was required. "
                        "The generated SQL passed validation "
                        "and execution."
                    )

                # Display execution results
                if result["success"]:

                    st.success("SQL query executed successfully!")

                    st.subheader("Query Results")

                    if result["rows"]:

                        dataframe = pd.DataFrame(
                            result["rows"],
                            columns=result["columns"]
                        )

                        st.dataframe(
                            dataframe,
                            use_container_width=True
                        )

                        st.info(
                            f"Total records returned: "
                            f"{len(result['rows'])}"
                        )

                    else:
                        st.warning("The query returned no records.")

                else:

                    st.error("Unable to execute the SQL query.")

                    st.error(result["error"])

            except Exception as error:

                st.error("An unexpected error occurred.")
                st.exception(error)

    else:

        st.warning("Please enter a question first.")

st.divider()

st.caption(
    "Developed using Python | PostgreSQL | RAG | Gemini | Streamlit"
)
