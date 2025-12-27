import sys

print("Testing RAG Pipeline...\n")

# Test 1: Document Building
print("[1] Testing document builder...")
from app.rag.document_builder import build_documents
docs = build_documents()
print(f"✓ Built {len(docs)} documents")
print(f"Sample: {docs[0].page_content[:80]}...\n")

# Test 2: Vector Store Creation
print("[2] Testing vector store...")
from app.rag.indexing import SYMPTOM_VECTOR_STORE
print(f"✓ Vector store has {SYMPTOM_VECTOR_STORE.index.ntotal} vectors\n")

# Test 3: Retrieval
print("[3] Testing retrieval...")
retriever = SYMPTOM_VECTOR_STORE.as_retriever(search_kwargs={"k": 2})
results = retriever.invoke("headache")
print(f"✓ Retrieved {len(results)} documents for 'headache'")
print(f"Top match: {results[0].metadata.get('symptom', 'N/A')}\n")

# Test 4: RAG Generation with Gemini
print("[4] Testing RAG generation...")
from app.rag.generation_service import generate_answer
answer = generate_answer("I have fever")
print(f"✓ Generated response")
print(f"Preview: {answer[:100]}...\n")

# Test 5: Full Service Layer
print("[5] Testing service layer...")
from app.services.symptom_service import analyze_symptoms
result = analyze_symptoms("headache and fever")
print(f"✓ Service working")
print(f"Answer: {result['answer'][:100]}...")
print(f"Disclaimer: {result['disclaimer']}\n")

print("=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print("\nNext steps:")
print("1. Run: uvicorn app.main:app --reload")
print("2. Test API: POST http://localhost:8000/check-symptoms")