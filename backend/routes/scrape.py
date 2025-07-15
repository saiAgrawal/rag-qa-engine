from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth_clerk import get_current_user_id, get_current_user
from backend.services.web_scraper import scrape_website_async
from backend.services.document_processor import DocumentProcessor

router = APIRouter()
doc_processor = DocumentProcessor()

class ScrapeRequest(BaseModel):
    url: str

@router.post("/scrape")
async def scrape_endpoint(
    data: ScrapeRequest,
    user_id: str = Depends(get_current_user_id)
):
    markdown_file = await scrape_website_async(data.url)
    success = doc_processor.process_document(markdown_file)
    return {"success": success, "url": data.url}
