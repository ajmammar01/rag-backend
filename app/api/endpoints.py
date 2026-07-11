from fastapi import APIRouter, UploadFile, File
from app.services.pdf_worker import extract_text_from_pdf, chunk_text
from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str

    
router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF, extract its text, and split it into chunks.
    """

    # Read uploaded file as bytes
    file_bytes = await file.read()

    # Extract text from PDF
    text = extract_text_from_pdf(file_bytes)

    # Split text into embedding-friendly chunks
    chunks = chunk_text(text)

    return {
        "filename": file.filename,
        "characters_extracted": len(text),
        "chunks_created": len(chunks),
        "preview": chunks[0] if chunks else ""
    }


@router.post("/query")
async def query(request: QueryRequest):
    return {
        "question": request.question,
        "answer": "This is a placeholder answer."
    }