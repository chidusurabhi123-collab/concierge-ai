from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag import answer_question

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        return answer_question(request.question)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Customer support service is temporarily unavailable."
        )