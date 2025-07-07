# app.py

import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

from document_processor import DocumentProcessor
from web_scraper import scrape_website_sync
from gemini_client import GeminiClient  # ✅ replaced openrouter with Gemini

load_dotenv()

st.set_page_config(page_title="RAG Q&A Engine", layout="wide")

# Initialize
@st.cache_resource
def init_components():
    return DocumentProcessor(), GeminiClient()

doc_processor, gemini_client = init_components()

st.title("🔍 RAG Q&A Engine")

# Sidebar
with st.sidebar:
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True,
                                       type=['pdf', 'docx', 'txt', 'md'])

    if uploaded_files and st.button("Process Documents"):
        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp:
                tmp.write(file.getvalue())
                if doc_processor.process_document(tmp.name):
                    st.success(f"✅ {file.name}")
                else:
                    st.error(f"❌ {file.name}")
                os.unlink(tmp.name)

    st.header("🌐 Scrape Website")
    url = st.text_input("Website URL")
    if st.button("Scrape") and url:
        with st.spinner("Scraping..."):
            markdown_file = scrape_website_sync(url)
            if markdown_file and doc_processor.process_document(markdown_file):
                st.success("✅ Website scraped!")
            else:
                st.error("❌ Failed to scrape")

# Chat interface
st.header("💬 Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        context_docs = doc_processor.query_documents(prompt)
        context = "\n".join(context_docs) if context_docs else ""
        response = gemini_client.generate_response(prompt, context)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
