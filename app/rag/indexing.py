#stores the knowledge
# app/rag/indexing.py

import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.rag.document_builder import build_documents

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

documents = build_documents()

embedding_dim = len(embeddings.embed_query("test"))

index = faiss.IndexFlatL2(embedding_dim)

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

vector_store.add_documents(documents)

SYMPTOM_VECTOR_STORE = vector_store

