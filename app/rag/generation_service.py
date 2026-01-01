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

# NEW: Separate prompt specifically for extracting remedies from MILD cases
remedies_prompt = ChatPromptTemplate.from_template("""
You are a medical assistant. Extract home remedies from the provided medical context.

Context (from medical knowledge base):
{context}

User's Symptoms:
{question}

TASK: Extract ONLY home remedies/self-care tips mentioned in the context.
Return them as a numbered list (1. remedy1, 2. remedy2, etc.)
If no remedies found in context, return: "No specific remedies available in database"

IMPORTANT: Only use remedies or self cure tips explicitly mentioned in the context. Do not add general advice.

Remedies:
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

# NEW: Separate chain for extracting remedies
remedies_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | remedies_prompt
    | llm
    | StrOutputParser()
)

def generate_answer(user_query: str, retrieved_docs: list = None):
    """Main function to generate answer using RAG pipeline"""
    try:
        answer = rag_chain.invoke(user_query)
        return answer
    except Exception as e:
        print(f"Generation error: {e}")
        return "Unable to process request. Please consult a healthcare professional."

def extract_remedies(user_query: str) -> list:
    """
    NEW FUNCTION: Extracts remedies from vector DB for MILD symptoms.
    
    Process:
    1. Vector DB retrieves top 3 relevant documents (same as RAG)
    2. LLM extracts only remedy/self-care information
    3. Parses into list format
    
    Args:
        user_query: User's symptom description
        
    Returns:
        list: List of remedies as strings
    """
    try:
        # Get remedies text from LLM
        remedies_text = remedies_chain.invoke(user_query)
        
        # Parse into list
        # LLM returns numbered format: "1. remedy1\n2. remedy2"
        remedies_list = []
        
        for line in remedies_text.split('\n'):
            line = line.strip()
            if line and not line.startswith("No specific"):
                # Remove numbering (1. 2. etc.) and keep remedy text
                clean_line = line.lstrip('0123456789.-)• ').strip()
                if clean_line:
                    remedies_list.append(clean_line)
        
        return remedies_list
        
    except Exception as e:
        print(f"Remedies extraction error: {e}")
        return []  # Return empty list on error