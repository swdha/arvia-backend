# check.py
from app.rag.indexing import SYMPTOM_VECTOR_STORE
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",  
    temperature=0
)

#  FAISS vector store
retriever = SYMPTOM_VECTOR_STORE.as_retriever(search_kwargs={"k": 3})

#  Define prompt template
prompt = ChatPromptTemplate.from_template("""
You are a medical assistant. Use only the context below to answer the question.

Context:
{context}

Question:
{question}
""")

# Define RAG query function
def rag_query(query_text):
    # Retrieve documents
    docs = retriever.get_relevant_documents(query_text)
    
    #  Combine retrieved docs into context
    context = "\n\n".join([doc.page_content for doc in docs])
    
    #  Fill prompt
    formatted_prompt = prompt.format_prompt(context=context, question=query_text).to_string()
    
    #  LLM expects a list of messages in chat format
    messages = [{"role": "user", "content": formatted_prompt}]
    
    #  Generate answer
    answer = llm.invoke(messages)
    
    #  Parse output
    return StrOutputParser().parse(answer)

#  Ask a question
query = "I have pain in my head since yesterday"
answer = rag_query(query)

print("QUESTION:")
print(query)
print("\nANSWER:")
print(answer)
