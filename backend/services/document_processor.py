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

    def get_source_from_filename(self, filename):
        """Extract source URL/domain from filename for better organization"""
        if 'crewai' in filename.lower():
            return 'CrewAI Documentation'
        elif 'techwithtim' in filename.lower():
            return 'Tech With Tim'
        else:
            return filename.replace('_', ' ').replace('.md', '')

    def process_document(self, file_path):
        try:
            print(f"📄 Processing document: {file_path}")
            text = self.extract_text(file_path)
            if not text: 
                print(f"❌ No text extracted from: {file_path}")
                return False

            print(f"📝 Extracted {len(text)} characters, creating chunks...")
            chunks = self.chunk_text(text)
            filename = os.path.basename(file_path)
            source_name = self.get_source_from_filename(filename)
            
            print(f"💾 Processing {len(chunks)} chunks for embedding from: {source_name}")
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    embedding = self.embedding_model.encode(chunk).tolist()
                    self.collection.add(
                        documents=[chunk],
                        embeddings=[embedding],
                        metadatas=[{
                            "source": filename,
                            "source_name": source_name,
                            "chunk_index": i,
                            "total_chunks": len(chunks)
                        }],
                        ids=[f"{filename}_{i}"]
                    )
                if (i + 1) % 10 == 0:  # Progress every 10 chunks
                    print(f"⏳ Processed {i + 1}/{len(chunks)} chunks...")
            
            print(f"✅ Successfully processed document: {filename} ({source_name})")
            return True
        except Exception as e:
            print("Document processing failed:", e)
            return False

    def query_documents(self, query, n_results=5):
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas']
            )
            
            # Return both documents and their sources for better context
            if results['documents'] and results['metadatas']:
                docs_with_sources = []
                for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                    docs_with_sources.append({
                        'content': doc,
                        'source': metadata.get('source_name', metadata.get('source', 'Unknown')),
                        'filename': metadata.get('source', 'Unknown')
                    })
                return docs_with_sources
            return []
        except Exception as e:
            print("Query failed:", e)
            return []

    def query_documents_by_source(self, query, source_filter=None, n_results=5):
        """Query documents with optional source filtering"""
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            
            where_clause = {}
            if source_filter:
                where_clause = {"source_name": {"$eq": source_filter}}
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause if where_clause else None,
                include=['documents', 'metadatas']
            )
            
            if results['documents'] and results['metadatas']:
                docs_with_sources = []
                for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                    docs_with_sources.append({
                        'content': doc,
                        'source': metadata.get('source_name', metadata.get('source', 'Unknown')),
                        'filename': metadata.get('source', 'Unknown')
                    })
                return docs_with_sources
            return []
        except Exception as e:
            print("Query failed:", e)
            return []

    def get_available_sources(self):
        """Get list of available document sources"""
        try:
            # Get all documents to find unique sources
            results = self.collection.get(include=['metadatas'])
            sources = set()
            for metadata in results['metadatas']:
                if 'source_name' in metadata:
                    sources.add(metadata['source_name'])
            return list(sources)
        except Exception as e:
            print("Failed to get sources:", e)
            return []

    def clear_all_documents(self):
        """Clear all documents from the collection"""
        try:
            # Get all document IDs
            results = self.collection.get()
            if results['ids']:
                # Delete all documents
                self.collection.delete(ids=results['ids'])
                print(f"✅ Cleared {len(results['ids'])} documents from database")
                return True
            else:
                print("📭 No documents to clear")
                return True
        except Exception as e:
            print(f"❌ Failed to clear documents: {e}")
            return False

    def clear_documents_by_source(self, source_name):
        """Clear documents from a specific source"""
        try:
            # Get documents from specific source
            results = self.collection.get(
                where={"source_name": {"$eq": source_name}},
                include=['ids']
            )
            if results['ids']:
                # Delete documents from this source
                self.collection.delete(ids=results['ids'])
                print(f"✅ Cleared {len(results['ids'])} documents from source: {source_name}")
                return True
            else:
                print(f"📭 No documents found for source: {source_name}")
                return True
        except Exception as e:
            print(f"❌ Failed to clear documents from {source_name}: {e}")
            return False