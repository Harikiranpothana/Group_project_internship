from fastapi import FastAPI
from app.api.query import router as query_router

app = FastAPI(
    title="InsightIQ API",
    description="Enterprise Business Intelligence Copilot",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "InsightIQ Backend is Live"
    }

app.include_router(query_router)