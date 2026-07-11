from fastapi import APIRouter, UploadFile, File
from app.services.pdf_worker import extract_text_from_pdf, chunk_text
from pydantic import BaseModel
from app.services.vector_db import save_chunks_to_vector_store

class QueryRequest(BaseModel):
    question: str

    
router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF, extract its text, split it into chunks,
    and save those chunks natively to ChromaDB.
    """

    # Read uploaded file as bytes
    file_bytes = await file.read()

    # Extract text from PDF
    text = extract_text_from_pdf(file_bytes)

    # Split text into embedding-friendly chunks
    chunks = chunk_text(text)

    # Clean and sanitize the filename to use as a unique ChromaDB collection name
    # (Removes spaces, extensions, and forces lowercase)
    collection_name = file.filename.replace(".pdf", "").replace(" ", "_").lower()

    # Save the chunks natively into your local Chroma DB database directory
    total_database_records = save_chunks_to_vector_store(collection_name, chunks)

    return {
        "status": "success",
        "filename": file.filename,
        "collection_created": collection_name,
        "characters_extracted": len(text),
        "chunks_created": len(chunks),
        "total_database_records": total_database_records,
        "preview": chunks[0] if chunks else ""
    }


@router.post("/query")
async def query(request: QueryRequest):
    return {
        "question": request.question,
        "answer": "This is a placeholder answer."
    }