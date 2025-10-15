# RAG-Based Chatbot 🤖

A Retrieval-Augmented Generation (RAG) chatbot built with Streamlit, LangChain, and Google's Gemini model. This chatbot can process PDF documents and answer questions based on their content.

## 🌟 Features

- **PDF Document Processing**: Upload and process PDF documents
- **Interactive Chat Interface**: Real-time conversation with typing effect
- **RAG Architecture**: Combines document retrieval with generative AI
- **Vector Storage**: Uses ChromaDB for efficient document retrieval
- **Secure API Handling**: Implements Streamlit secrets management
- **Responsive UI**: Clean and user-friendly interface

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM**: Google Gemini (via LangChain)
- **Embeddings**: Hugging Face (sentence-transformers/all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB
- **Document Processing**: LangChain's PyPDFLoader
- **Python Libraries**: LangChain, google-generativeai, streamlit

## 📋 Prerequisites

- Python 3.8+
- Google API Key (Gemini access)
- Required Python packages (see requirements.txt)

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ADEEL-308/RAG_BASED_CHATBOT.git
   cd RAG_BASED_CHATBOT
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   - Create a `.streamlit/secrets.toml` file
   - Add your Google API key:
     ```toml
     GOOGLE_API_KEY = "your-api-key-here"
     ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📝 Usage

1. Launch the application
2. Upload a PDF document using the sidebar
3. Wait for the document to be processed
4. Start asking questions about the document content
5. The chatbot will provide relevant answers based on the document

## 🎯 Project Structure

```
RAG_BASED_CHATBOT/
├── app.py              # Main Streamlit application
├── chatbot.py         # Chatbot logic and RAG implementation
├── requirements.txt   # Project dependencies
├── .streamlit/       # Streamlit configuration
│   └── secrets.toml  # API keys (not in repo)
├── data/            # PDF storage directory
└── chroma_db/       # Vector database storage
```

## ⚙️ Configuration

The chatbot can be configured through the following parameters in `chatbot.py`:
- Chunk size for document splitting
- Number of relevant chunks to retrieve
- Temperature for response generation
- Model selection (Gemini version)

## 🔒 Security

- API keys are managed through Streamlit's secrets management
- Sensitive files are included in .gitignore
- PDF documents are stored locally

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [LangChain](https://python.langchain.com/) framework
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)