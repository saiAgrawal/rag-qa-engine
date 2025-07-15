# document_processor.py

import os
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer
import chromadb

class DocumentProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection("documents")

    def extract_text(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            with open(file_path, 'rb') as file:
                return "\n".join(page.extract_text() for page in PyPDF2.PdfReader(file).pages)
        elif ext == '.docx':
            return "\n".join(p.text for p in docx.Document(file_path).paragraphs)
        elif ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        return None

    def chunk_text(self, text, size=1000):
        words = text.split()
        return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

    def process_document(self, file_path):
        try:
            text = self.extract_text(file_path)
            if not text: return False

            chunks = self.chunk_text(text)
            filename = os.path.basename(file_path)

            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    embedding = self.embedding_model.encode(chunk).tolist()
                    self.collection.add(
                        documents=[chunk],
                        embeddings=[embedding],
                        metadatas=[{"source": filename}],
                        ids=[f"{filename}_{i}"]
                    )
            return True
        except Exception as e:
            print("Document processing failed:", e)
            return False

    def query_documents(self, query, n_results=5):
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            print("Query failed:", e)
            return []