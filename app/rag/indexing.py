import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# HuggingFace embedding model (dimension 384)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_FOLDER = os.path.join(BASE_DIR, "vector_db")
VECTOR_DB_PATH = os.path.join(VECTOR_DB_FOLDER, "symptom_vectorstore")

if not os.path.exists(f"{VECTOR_DB_PATH}.faiss"):
    raise FileNotFoundError(f"Cannot find {VECTOR_DB_PATH}.faiss")

print("Loading vector database...")

vector_store = FAISS.load_local(
    folder_path=VECTOR_DB_FOLDER,
    index_name="symptom_vectorstore",
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

print(f"Loaded {vector_store.index.ntotal} vectors")

SYMPTOM_VECTOR_STORE = vector_store