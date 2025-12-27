from sentence_transformers import SentenceTransformer
from app.rag.document_builder import build_documents

# Load embedding model (small + fast)
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_document_embeddings():
    """
    Converts documents into vector embeddings.
    """
    documents = build_documents()

    embeddings = model.encode(documents)

    return documents, embeddings
