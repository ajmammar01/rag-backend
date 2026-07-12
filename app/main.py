from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI()

# Register all routes from endpoints.py
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}