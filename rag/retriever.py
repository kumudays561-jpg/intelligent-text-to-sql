
import json
import numpy as np

from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

VECTOR_PATH = "vector_db/schema_embeddings.npy"
METADATA_PATH = "vector_db/metadata.json"
SCHEMA_PATH = "datasets/schema.json"


class SchemaRetriever:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            MODEL_NAME,
            device="cpu"
        )

        self.embeddings = np.load(VECTOR_PATH)

        with open(METADATA_PATH, "r") as file:
            self.documents = json.load(file)

        with open(SCHEMA_PATH, "r") as file:
            self.schema = json.load(file)

        print("Schema retriever initialized successfully!")

    def expand_relationships(self, table_names):

        expanded = set()
        queue = list(table_names)

        while queue:

            table = queue.pop(0)

            if table in expanded:
                continue

            expanded.add(table)

            details = self.schema.get(table, {})

            # Follow foreign keys to referenced tables
            for fk in details.get("foreign_keys", []):

                referenced_table = fk["references_table"]

                if referenced_table not in expanded:
                    queue.append(referenced_table)

        return expanded

    
    def retrieve(self, question, top_k=3):

        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        similarities = np.dot(
            self.embeddings,
            query_embedding.T
        ).flatten()

        ranked_indices = np.argsort(similarities)[::-1]

        # Select the strongest semantic match
        best_index = ranked_indices[0]

        selected_tables = [
            self.documents[best_index]["table"]
        ]

        # Recursively discover required related tables
        relevant_tables = self.expand_relationships(
            selected_tables
        )

        context = {}

        for table in sorted(relevant_tables):
            context[table] = self.schema[table]

        return {
            "matched_tables": selected_tables,
            "relevant_tables": sorted(relevant_tables),
            "similarities": [
                float(similarities[index])
                for index in ranked_indices[:top_k]
            ],
            "schema_context": context
        }



if __name__ == "__main__":

    retriever = SchemaRetriever()

    question = input("\nEnter your question: ")

    result = retriever.retrieve(question)

    print("\nMatched tables:")
    print(result["matched_tables"])

    print("\nRelevant tables after relationship expansion:")
    print(result["relevant_tables"])

    print("\nSimilarity scores:")
    print(result["similarities"])

    print("\nRetrieved schema context:")

    print(
        json.dumps(
            result["schema_context"],
            indent=4
        )
    )
