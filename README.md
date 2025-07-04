# 🔍 RAG Q&A Engine

A powerful Retrieval-Augmented Generation (RAG) application that allows you to upload documents or scrape websites, store content in a vector database (ChromaDB), and ask questions using OpenRouter-powered AI models like Mistral, Mixtral, etc.

---

## 🚀 Features

- 📄 Upload PDFs, DOCX, TXT, or Markdown files  
- 🌐 Scrape web pages to extract and store content  
- 🧠 Embed content using SentenceTransformers  
- 🔎 Search chunks using ChromaDB (vector DB)  
- 💬 Ask questions in a Streamlit chat interface  
- 🔗 Powered by OpenRouter API (supports Mistral, Claude, LLaMA, Mixtral, etc.)

---

## 📁 Project Structure

```
rag-qa-engine/
├── app.py                   # Streamlit frontend
├── document_processor.py    # Embedding, chunking, and retrieval logic
├── openrouter_client.py     # API interface for OpenRouter
├── web_scraper.py           # Website scraping + .md file creation
├── .env                     # API key (not checked in)
├── requirements.txt         # Dependencies
└── scraped_content/         # Saved markdowns from scraped sites
```

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/rag-qa-engine.git
cd rag-qa-engine
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
# Activate the environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your OpenRouter API Key

Create a `.env` file in the root directory and paste your key:

```
OPENROUTER_API_KEY=sk-or-your-api-key-here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

## ✅ Supported Input Formats

- `.pdf`
- `.docx`
- `.txt`
- `.md`
- Website URLs (converted to markdown)

---

## 🧠 Tech Stack

- **Frontend**: Streamlit  
- **Vector DB**: ChromaDB  
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`)  
- **LLM API**: [OpenRouter API](https://openrouter.ai)  
- **Scraping**: `requests` + `BeautifulSoup`

---

## 🌍 Models via OpenRouter

This app supports any OpenRouter-compatible models.  
Default model used:

```
mistralai/mistral-7b-instruct
```

You can change this inside `openrouter_client.py` as:

```python
self.model = "anthropic/claude-3-haiku"  # or another model
```

---

## 🛡️ Environment Variables

| Key | Description |
|-----|-------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |

---

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai)  
- [Streamlit](https://streamlit.io)  
- [ChromaDB](https://www.trychroma.com)  
- [Sentence Transformers](https://www.sbert.net)

---

## 📜 License

This project is licensed under the **MIT License**.
