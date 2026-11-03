
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router as rag_router
from app.api.order_routes import router as order_router
from app.api.escalation_routes import router as escalation_router


# Initialize application
app = FastAPI(
    title="Concierge AI",
    description="AI-powered customer support assistant",
    version="0.3.0"
)


# Frontend configuration
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


# Frontend homepage
@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


# Register API routes
app.include_router(rag_router, prefix="/api")
app.include_router(order_router, prefix="/api")
app.include_router(escalation_router, prefix="/api")


# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
