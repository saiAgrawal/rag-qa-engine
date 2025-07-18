# backend/routes/chat.py

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth_clerk import get_current_user_id, get_current_user
from backend.services.gemini_client import GeminiClient
from backend.services.document_processor import DocumentProcessor

router = APIRouter()
gemini = GeminiClient()
doc_processor = DocumentProcessor()

class ChatRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_endpoint(
    data: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    # Query documents with source information
    docs_with_sources = doc_processor.query_documents(data.prompt, n_results=5)
    
    if docs_with_sources:
        # Format context without source names in the content
        context_parts = []
        sources_used = set()
        
        for doc_info in docs_with_sources:
            content = doc_info['content']
            source = doc_info['source']
            sources_used.add(source)
            context_parts.append(content)  # Just the content, no source labels
        
        context = "\n\n".join(context_parts)
        
        # Simple prompt without source mentions
        enhanced_prompt = f"""
Based on the following documents, please answer the question: {data.prompt}

{context}

Please provide a clear and concise answer.
"""
        
        answer = gemini.generate_response(enhanced_prompt, context)
        
        # Add source information to response (but not shown in UI)
        response = {
            "answer": answer,
            "sources_used": list(sources_used),
            "num_documents": len(docs_with_sources)
        }
    else:
        answer = gemini.generate_response(data.prompt, "")
        response = {
            "answer": answer,
            "sources_used": [],
            "num_documents": 0
        }
    
    return response

@router.get("/sources")
async def get_sources(user_id: str = Depends(get_current_user_id)):
    """Get list of available document sources"""
    sources = doc_processor.get_available_sources()
    return {"sources": sources}

@router.post("/chat-by-source")
async def chat_by_source_endpoint(
    data: ChatRequest,
    source_filter: str = None,
    user_id: str = Depends(get_current_user_id)
):
    """Chat with documents filtered by source"""
    if source_filter:
        docs_with_sources = doc_processor.query_documents_by_source(
            data.prompt, 
            source_filter=source_filter, 
            n_results=5
        )
    else:
        docs_with_sources = doc_processor.query_documents(data.prompt, n_results=5)
    
    if docs_with_sources:
        # Format context without source names
        context_parts = []
        sources_used = set()
        
        for doc_info in docs_with_sources:
            content = doc_info['content']
            source = doc_info['source']
            sources_used.add(source)
            context_parts.append(content)
        
        context = "\n\n".join(context_parts)
        
        # Simple prompt
        enhanced_prompt = f"""
Based on the following documents, please answer the question: {data.prompt}

{context}

Please provide a clear and concise answer.
"""
        
        answer = gemini.generate_response(enhanced_prompt, context)
        
        response = {
            "answer": answer,
            "sources_used": list(sources_used),
            "num_documents": len(docs_with_sources),
            "source_filter": source_filter
        }
    else:
        answer = f"No documents found for your query about '{data.prompt}'" + (f" in source '{source_filter}'" if source_filter else "")
        response = {
            "answer": answer,
            "sources_used": [],
            "num_documents": 0,
            "source_filter": source_filter
        }
    
    return response
