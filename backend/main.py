import os
import sys
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from database.db import init_db
from api.router import api_router
from api.predict_router import router as predict_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("evidence_boundary.main")

# Initialize SQLite Database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Don't just verify the claim. Find where the evidence ends.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error processing {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Evidence Boundary server error", "error": str(exc)}
    )

# Include API Router and Root Predict Router
app.include_router(api_router)
app.include_router(predict_router)  # Mounted at root for POST /predict and GET /health

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.APP_NAME} (DEMO_MODE={settings.DEMO_MODE})...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
