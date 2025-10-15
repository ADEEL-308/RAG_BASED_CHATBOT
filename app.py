import streamlit as st
import time
from chatbot import get_qa_chain, process_new_pdf

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "greeted" not in st.session_state:
        st.session_state.greeted = False
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = get_qa_chain()

def setup_page():
    """Configure the basic page layout."""
    st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="centered")
    st.title("🤖 RAG Chatbot")
    st.caption("Ask questions about your uploaded documents in real time!")

def handle_file_upload():
    """Handle PDF file upload and processing."""
    st.sidebar.header("📂 Manage Documents")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file:
        file_path = f"./data/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        process_new_pdf(file_path)
        st.sidebar.success(f"✅ {uploaded_file.name} added and processed!")
        
        # Show greeting only after successful file upload
        if not st.session_state.greeted:
            st.session_state.greeted = True
            add_message("assistant", "Greetings! I've processed your document. How can I help you?")

def add_message(role, content):
    """Add a message to the chat history."""
    st.session_state.chat_history.append({"role": role, "content": content})

def handle_user_input():
    """Process user input and generate response."""
    user_query = st.chat_input("Type your question here...")
    
    if user_query:
        add_message("user", user_query)
        with st.spinner("💭 Thinking..."):
            response = st.session_state.qa_chain.invoke({"query": user_query})
            answer = response["result"]
        add_message("assistant", answer)

def display_chat_history():
    """Display all messages except the last one."""
    for msg in st.session_state.chat_history[:-1]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def display_latest_message():
    """Display the latest message with typing effect if it's from assistant."""
    if st.session_state.chat_history:
        last_msg = st.session_state.chat_history[-1]
        if last_msg["role"] == "assistant":
            with st.chat_message("assistant"):
                placeholder = st.empty()
                typed_text = ""
                for char in last_msg["content"]:
                    typed_text += char
                    placeholder.markdown(typed_text)
                    time.sleep(0.015)  # typing speed

def main():
    """Main application function."""
    setup_page()
    initialize_session_state()
    handle_file_upload()
    handle_user_input()
    display_chat_history()
    display_latest_message()

if __name__ == "__main__":
    main()
