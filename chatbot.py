# chatbot.py
import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# -------------------------------
# 1️⃣ Environment setup
# -------------------------------
# Use Streamlit secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

DATA_DIR = "./data"
CHROMA_DIR = "./chroma_db"

# -------------------------------
# 2️⃣ Embedding model (free + local)
# -------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------------
# 3️⃣ Custom Gemini-friendly prompt
# -------------------------------
QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a precise and knowledgeable assistant for Byte & Spice Bistro. Follow these guidelines:

1. Use ONLY information from the provided context
2. Be concise and direct in your responses
3. If information is found in context:
   - Answer with specific details from the document
   - Include relevant prices, times, or quantities if present
   - Format lists or menu items in a clear, readable way
4. If information is partially available:
   - State what is known from the context
   - Clearly indicate what parts are not mentioned
5. If information is not in context:
   - Respond: "I don't have this information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
""",
)



# -------------------------------
# 4️⃣ Chroma vector store handling
# -------------------------------
def get_vectorstore():
    """Load existing Chroma DB or create a new one."""
    if os.path.exists(CHROMA_DIR) and len(os.listdir(CHROMA_DIR)) > 0:
        print("🔁 Loading existing Chroma vector store...")
        db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    else:
        print("📄 Creating new Chroma vector store...")
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(CHROMA_DIR, exist_ok=True)
        db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return db


# -------------------------------
# 5️⃣ Add new PDFs to vector store
# -------------------------------
def process_new_pdf(file_path):
    print(f"📥 Processing new PDF: {file_path}")

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    db = get_vectorstore()

    # Simple deduplication check
    if db._collection.count() > 0:
        print("⚠️ Database already has content; skipping duplicate re-embedding.")
        return

    db.add_documents(chunks)
    global qa_chain
    qa_chain = get_qa_chain()
    print(f"✅ Added {file_path} to Chroma DB and refreshed retriever.")



# -------------------------------
# 6️⃣ Build the RAG QA Chain
# -------------------------------
def get_qa_chain():
    """Builds the RetrievalQA chain using Gemini + Chroma retriever."""
    db = get_vectorstore()
    retriever = db.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # or "gemini-1.5-flash" if preferred
        temperature=0.4
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True
    )

    return qa_chain


# -------------------------------
# 7️⃣ Initialize global QA chain
# -------------------------------
qa_chain = get_qa_chain()

print("🤖 Gemini RAG Chatbot initialized successfully.")
