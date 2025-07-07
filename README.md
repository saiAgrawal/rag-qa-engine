# 🔍 RAG Q&A Engine 

This is a lightweight, local-first Retrieval-Augmented Generation (RAG) chatbot that can process documents and websites, embed them into a vector database, and generate answers using Google Gemini 1.5 Flash.

---

## ✨ Features

- 📄 Upload and process PDF, DOCX, TXT, and Markdown files
- 🌐 Scrape websites and store readable content
- 🔎 Vector search with ChromaDB and Sentence Transformers
- 🤖 Answer generation using Gemini 1.5 Flash via API
- 💬 Interactive chat interface powered by Streamlit

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/rag-qa-engine.git
cd rag-qa-engine
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # On Windows
# source .venv/bin/activate  # On macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 🔐 Setup API Key
Create a file named `.env` in the project root and add your Gemini API Key:

```
GEMINI_API_KEY=your_api_key_here
```

### 🚀 Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal, usually:

```
http://localhost:8501
```

---

## 📂 Project Structure

```
rag-qa-engine/
├── app.py                  # Main Streamlit interface
├── document_processor.py   # Handles file parsing and vector indexing
├── gemini_client.py        # API wrapper for Gemini 1.5 Flash
├── web_scraper.py          # Website scraping logic
├── requirements.txt        # Dependencies
├── .env                    # Your Gemini API key
└── chroma_db/              # Local vector database (auto-created)
```

---

## 🔎 How It Works
1. Upload or scrape content → extract plain text
2. Chunk the text and embed using sentence-transformers
3. Store chunks in ChromaDB with metadata
4. On user query, retrieve relevant documents
5. Send context + query to Gemini 1.5 Flash
6. Display the answer in chat interface

---

## 📄 Supported File Types
- .pdf
- .docx
- .txt
- .md

---

## 🤝 Contributing
Pull requests and feedback welcome!

---

## 📃 License
Licensed under the MIT License.

---

## 💡 Tips
- Use well-formatted PDFs and clear website URLs for best results.
- You can clear your ChromaDB directory (`chroma_db/`) if needed.
- If your API key fails, ensure your Makersuite account has API access enabled.

---

## ⭐ Credits
- Google Gemini API via google-generativeai
- Vector DB via Chroma
- Embeddings via sentence-transformers
- UI via Streamlit

---

## 🙌 Author
Made with ❤️ by Sai Agrawal
