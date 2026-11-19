from sentence_transformers import SentenceTransformer
from rag.schema_documents import create_schema_documents

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def generate_embeddings():

    model = SentenceTransformer(MODEL_NAME, device="cpu")

    documents = create_schema_documents()

    texts = [doc["content"] for doc in documents]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return documents, embeddings


if __name__ == "__main__":

    documents, embeddings = generate_embeddings()

    print("Number of documents:", len(documents))
    print("Embedding shape:", embeddings.shape)
    print("Embedding generation successful!")