from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.escalation_service import (
    create_escalation,
    get_escalations
)

router = APIRouter()


class EscalationRequest(BaseModel):
    question: str
    reason: str = "Insufficient information"


@router.post("/escalations")
def submit_escalation(request: EscalationRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    return create_escalation(
        request.question,
        request.reason
    )


@router.get("/escalations")
def list_escalations():
    return {
        "total": len(get_escalations()),
        "tickets": get_escalations()
    }