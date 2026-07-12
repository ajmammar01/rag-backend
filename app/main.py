from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI()

# Register all routes from endpoints.py
app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "rag-backend-api",
        "version": "1.0.0"
    }