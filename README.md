# 🧠 RAG Q&A Engine

A comprehensive Retrieval-Augmented Generation (RAG) system with authentication, document processing, and intelligent question-answering capabilities.

## 🌟 Features

- **� Clerk Authentication**: Secure user authentication and session management
- **📄 Document Processing**: Support for PDF, DOCX, TXT, and MD files
- **🌐 Web Scraping**: Extract and process content from websites
- **💬 Intelligent Chat**: AI-powered question-answering using Google Gemini
- **🎨 Modern UI**: Beautiful Next.js dashboard and Streamlit interface
- **⚡ Real-time Processing**: Fast document embedding and retrieval

## 🏗️ Architecture

The system consists of three main components:

1. **FastAPI Backend** (Port 8000): Core API with authentication and document processing
2. **Next.js Frontend** (Port 3000): Modern dashboard with Clerk authentication
3. **Streamlit App** (Port 8501): Interactive RAG interface for document Q&A

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Google Gemini API key
- Clerk account for authentication

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rag-qa-engine.git
   cd rag-qa-engine
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Next.js dependencies**
   ```bash
   cd next-clerk-auth
   npm install
   cd ..
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Google Gemini API
   GOOGLE_API_KEY=your_gemini_api_key_here
   
   # Clerk Authentication
   CLERK_SECRET_KEY=your_clerk_secret_key
   CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
   CLERK_JWKS_URL=https://your-clerk-domain.clerk.accounts.dev/.well-known/jwks.json
   ```
   
   Create `.env.local` in the `next-clerk-auth` directory:
   ```env
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
   CLERK_SECRET_KEY=your_clerk_secret_key
   ```

### Running the Application

You can start all services at once using the provided scripts:

**Windows:**
```bash
# Using batch file
start-all.bat

# Or using PowerShell
start-all.ps1
```

**Unix/Linux/macOS:**
```bash
# Make script executable
chmod +x launch-all.sh

# Run all services
./launch-all.sh
```

**Manual startup:**
```bash
# Terminal 1: FastAPI Backend
uvicorn main:app --reload --port 8000

# Terminal 2: Next.js Frontend
cd next-clerk-auth && npm run dev

# Terminal 3: Streamlit App
streamlit run app.py --server.port 8501
```

### Access the Application

- **Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Streamlit RAG Interface**: http://localhost:8501 (access via dashboard)

## 📖 Usage

1. **Sign up/Sign in** at http://localhost:3000
2. **Upload Documents** or **Scrape Websites** via the dashboard
3. **Open RAG Q&A Engine** to start asking questions about your documents
4. **Chat** with your documents using natural language

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **ChromaDB**: Vector database for document embeddings
- **Sentence Transformers**: Text embedding models
- **Google Gemini**: LLM for question answering
- **PyJWT**: JWT token handling

### Frontend
- **Next.js 14**: React framework with App Router
- **Tailwind CSS**: Utility-first CSS framework
- **Clerk**: Authentication and user management
- **TypeScript**: Type-safe JavaScript

### RAG Interface
- **Streamlit**: Interactive web app framework
- **BeautifulSoup4**: Web scraping
- **HTTPX**: Async HTTP client

## 📁 Project Structure

```
rag-qa-engine/
├── main.py                 # FastAPI main application
├── app.py                  # Streamlit RAG interface
├── auth_clerk.py          # Clerk authentication handler
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── backend/
│   ├── routes/           # API routes
│   │   ├── chat.py       # Chat endpoints
│   │   ├── upload.py     # File upload endpoints
│   │   └── scrape.py     # Web scraping endpoints
│   └── services/         # Business logic
│       ├── document_processor.py
│       ├── gemini_client.py
│       └── web_scraper.py
├── next-clerk-auth/      # Next.js frontend
│   ├── app/              # App Router pages
│   ├── middleware.ts     # Clerk middleware
│   └── package.json      # Node dependencies
├── scripts/              # Utility scripts
│   ├── start-all.bat     # Windows startup
│   ├── start-all.ps1     # PowerShell startup
│   └── launch-all.sh     # Unix/Linux startup
└── chroma_db/            # Vector database (auto-created)
```

## 🔧 Configuration

### Clerk Setup

1. Create a Clerk application at [clerk.com](https://clerk.com)
2. Configure JWT templates in Clerk dashboard
3. Set up allowed origins: `http://localhost:3000`, `http://localhost:8501`
4. Copy API keys to environment variables

### Google Gemini Setup

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file as `GOOGLE_API_KEY`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Clerk](https://clerk.com) for authentication
- [Google Gemini](https://ai.google.dev/) for AI capabilities
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Streamlit](https://streamlit.io/) for the RAG interface
- [Next.js](https://nextjs.org/) for the modern frontend

## 📧 Support

For support and questions, please open an issue on GitHub or contact [your-email@example.com](mailto:your-email@example.com).

---

**Built with ❤️ using RAG, AI, and modern web technologies**

This is a full-stack Retrieval-Augmented Generation (RAG) chatbot with FastAPI backend, Streamlit frontend, and Clerk authentication. It can process documents and websites, embed them into a vector database, and generate answers using Google Gemini 1.5 Flash.

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
