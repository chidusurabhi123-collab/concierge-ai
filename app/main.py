from fastapi import FastAPI

from app.api.routes import router as rag_router
from app.api.order_routes import router as order_router
from app.api.escalation_routes import router as escalation_router

app = FastAPI(
    title="Concierge AI",
    description="AI-powered customer support assistant",
    version="0.3.0"
)

app.include_router(rag_router, prefix="/api")
app.include_router(escalation_router, prefix="/api")
app.include_router(order_router, prefix="/api")


@app.get("/")
def home():
    return {
        "message": "Concierge AI is running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}