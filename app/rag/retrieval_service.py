from sentence_transformers import util
from app.rag.embedding_service import generate_document_embeddings

# Load documents & embeddings once
DOCUMENTS, DOCUMENT_EMBEDDINGS = generate_document_embeddings()


def retrieve_relevant_documents(query: str, top_k: int = 2):
    """
    Finds the most relevant documents for a user query.
    """
    query_embedding = util.normalize_embeddings(
        util.tensor([query])
    )

    # Compute similarity scores
    scores = util.cos_sim(query_embedding, DOCUMENT_EMBEDDINGS)[0]

    # Get top matching document indices
    top_results = scores.topk(k=top_k)

    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        results.append({
            "document": DOCUMENTS[idx],
            "score": float(score)
        })

    return results #(passed to generation service)
