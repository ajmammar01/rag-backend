from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.endpoints import router

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # In production, you would log 'exc' to a monitoring tool like Sentry
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred while processing your RAG pipeline.",
            "details": str(exc)  # Drop this details line if you want to hide internal stack traces from users
        }
    )

# Register all routes from endpoints.py
app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "rag-backend-api",
        "version": "1.0.0"
    }