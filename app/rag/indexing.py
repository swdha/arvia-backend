from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.rag.document_builder import build_documents

# Initialize Google's embedding model (converts text to vectors)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

# Build documents from symptom database
documents = build_documents()

# Create FAISS vector store
# This: 1) converts docs to embeddings, 2) builds searchable index which faiss stores
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

# Export for use in other modules
SYMPTOM_VECTOR_STORE = vector_store