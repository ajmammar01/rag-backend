from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Dummy upload endpoint.
    Accepts a file and returns its filename.
    """
    return {
        "filename": file.filename
    }


@router.post("/query")
async def query(request: QueryRequest):
    """
    Dummy query endpoint.
    Accepts a question and returns a placeholder answer.
    """
    return {
        "question": request.question,
        "answer": "This is a placeholder answer."
    }