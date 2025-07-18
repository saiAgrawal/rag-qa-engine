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
    # Clear all existing documents before scraping new content
    print("🗑️ Clearing existing documents before scraping...")
    doc_processor.clear_all_documents()
    
    print(f"🔄 Starting scrape of: {data.url}")
    markdown_file = await scrape_website_async(data.url)
    
    if markdown_file:
        print(f"📝 Processing scraped content...")
        success = doc_processor.process_document(markdown_file)
        return {"success": success, "url": data.url, "message": "Website scraped and old data cleared"}
    else:
        return {"success": False, "url": data.url, "message": "Failed to scrape website"}

@router.post("/clear-all")
async def clear_all_documents(user_id: str = Depends(get_current_user_id)):
    """Clear all documents from the database"""
    success = doc_processor.clear_all_documents()
    return {"success": success, "message": "All documents cleared" if success else "Failed to clear documents"}

@router.post("/clear-source")
async def clear_source_documents(
    source_name: str,
    user_id: str = Depends(get_current_user_id)
):
    """Clear documents from a specific source"""
    success = doc_processor.clear_documents_by_source(source_name)
    return {"success": success, "message": f"Documents from {source_name} cleared" if success else f"Failed to clear documents from {source_name}"}
