from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.rag.indexing import SYMPTOM_VECTOR_STORE

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Latest stable model with good free tier
    temperature=0.3
)

# Create retriever from vector store (returns top 3 similar docs)
retriever = SYMPTOM_VECTOR_STORE.as_retriever(search_kwargs={"k": 3})

# Prompt template for structured medical responses
prompt = ChatPromptTemplate.from_template("""
You are a medical information assistant. Use only the provided context to help users understand their symptoms.

Context:
{context}

User Query:
{question}

Provide a structured response with:
- Detected Symptoms
- Possible Causes (non-diagnostic)
- Recommended Doctor Type
- Self-Care Tips
- Disclaimer: This is not a medical diagnosis. Consult a healthcare professional.
""")

def format_docs(docs):
    """Combine retrieved documents into single context string"""
    return "\n\n".join(doc.page_content for doc in docs)

# RAG chain: retrieve → format → prompt → generate → parse
rag_chain = (
    {
        "context": retriever | format_docs,  # Get docs and format them i.e. combine top 3 docs into one string
        "question": RunnablePassthrough()     # Pass query through unchanged
    }
    | prompt              # Fill template with context and question
    | llm                 # Send to Gemini
    | StrOutputParser()   # Extract string from response
    # langchain expression language lcel
)

def generate_answer(user_query: str, retrieved_docs: list = None):
    """Main function to generate answer using RAG pipeline"""
    try:
        answer = rag_chain.invoke(user_query)
        return answer
    except Exception as e:
        print(f"Generation error: {e}")
        return "Unable to process request. Please consult a healthcare professional."