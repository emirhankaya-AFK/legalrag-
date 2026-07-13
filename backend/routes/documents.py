from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
from ..services.storage_service import storage_service
from ..services.rag_service import rag_service

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        content = await file.read()
        file_size = len(content)
        
        # Max file size 20MB
        if file_size > 20 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 20MB limit.")
            
        # Save file to upload directory
        saved_path = storage_service.save_file(content, file.filename)
        
        # Add to SQLite metadata database
        doc_data = storage_service.add_document(
            filename=file.filename,
            file_path=str(saved_path),
            file_size=file_size
        )
        
        return {
            "message": "Document uploaded successfully",
            "document": doc_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {e}")

@router.get("", response_model=List[dict])
def list_documents():
    return storage_service.list_documents()

@router.get("/{document_id}")
def get_document(document_id: int):
    doc = storage_service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{document_id}")
def delete_document(document_id: int):
    # Retrieve doc first
    doc = storage_service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    # Delete database references and the file
    success = storage_service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete document from database")
        
    # Clear index in ChromaDB
    try:
        rag_service.delete_document_clauses(document_id)
    except Exception as e:
        print(f"Error deleting clauses from ChromaDB: {e}")
        
    return {"message": "Document deleted successfully"}
