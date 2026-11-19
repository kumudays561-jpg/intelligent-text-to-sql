
import json
import numpy as np
import os

from rag.embeddings import generate_embeddings

VECTOR_PATH = "vector_db/schema_embeddings.npy"
METADATA_PATH = "vector_db/metadata.json"


def create_vector_store():
    documents, embeddings = generate_embeddings()

    embeddings = np.asarray(embeddings, dtype="float32")

    os.makedirs("vector_db", exist_ok=True)

    np.save(VECTOR_PATH, embeddings)

    with open(METADATA_PATH, "w") as file:
        json.dump(documents, file, indent=4)

    print("NumPy vector store created successfully!")
    print("Total indexed documents:", len(documents))
    print("Embedding shape:", embeddings.shape)


if __name__ == "__main__":
    create_vector_store()
