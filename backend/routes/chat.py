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

    docs = doc_processor.query_documents(data.prompt)
    context = "\n".join(docs) if docs else ""
    answer = gemini.generate_response(data.prompt, context)
    return {"answer": answer}
