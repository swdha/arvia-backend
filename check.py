# check.py - Test RAG pipeline directly

from app.rag.indexing import SYMPTOM_VECTOR_STORE
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Latest stable model
    temperature=0
)

# Create retriever
retriever = SYMPTOM_VECTOR_STORE.as_retriever(search_kwargs={"k": 3})

# Define prompt
prompt = ChatPromptTemplate.from_template("""
You are a medical assistant. Use only the context below to answer the question.

Context:
{context}

Question:
{question}
""")

def format_docs(docs):
    """Convert list of docs to single string"""
    return "\n\n".join(doc.page_content for doc in docs)

# Build RAG chain using LCEL (LangChain Expression Language)
# Flow: retrieve docs → format → fill prompt → LLM → parse
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    query = "I have pain in my head since yesterday"
    answer = rag_chain.invoke(query)
    
    print("QUESTION:", query)
    print("\nANSWER:", answer)