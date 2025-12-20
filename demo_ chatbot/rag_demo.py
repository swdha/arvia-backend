# NO OPENAI API KEY NEEDED FOR THIS VERSION

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


# 1. Load website content
loader = WebBaseLoader("https://docs.langchain.com/oss/python/langchain/rag")
docs = loader.load()
print(f"Loaded {len(docs)} document(s)")


# 2. Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)
print(f"Split into {len(splits)} chunks")


# 3. FREE local embeddings (no API key)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(splits, embeddings)
print("Vector store created")


# 4. Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# 5. LLM (still OpenAI — comment this if you want FULLY offline)
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# 6. Prompt template
prompt = ChatPromptTemplate.from_template("""
You are an assistant that answers questions using only the provided context.

Context:
{context}

Question:
{question}
""")


# 7. RAG chain
rag_chain = (
    {
        "context": retriever,
        "question": lambda x: x
    }
    | prompt
    | llm
    | StrOutputParser()
)


# 8. Ask a question
query = "Hello, how are you?"
answer = rag_chain.invoke(query)

print("\nANSWER:")
print(answer)
