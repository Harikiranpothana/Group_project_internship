from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.query import router as query_router


app = FastAPI(
    title="InsightIQ API",
    description="Enterprise Business Intelligence Copilot",
    version="1.0.0"
)

# -----------------------------
# CORS Configuration
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "message": "InsightIQ Backend is Live"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# -----------------------------
# API Routes
# -----------------------------

app.include_router(
    query_router,
    prefix="/api",
    tags=["Query API"]
)