from fastapi import APIRouter, UploadFile, File, Depends
from auth_clerk import get_current_user_id, get_current_user
from backend.services.document_processor import DocumentProcessor
import os

router = APIRouter()
doc_processor = DocumentProcessor()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    contents = await file.read()

    os.makedirs("temp_files", exist_ok=True)
    file_path = f"temp_files/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(contents)

    success = doc_processor.process_document(file_path)

    return {
        "filename": file.filename,
        "status": "embedded" if success else "failed"
    }
