from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..agents.qa_agent import qa_agent

router = APIRouter(prefix="/qa", tags=["qa"])

class QARequest(BaseModel):
    document_id: int
    question: str

@router.post("")
def ask_question(request: QARequest):
    try:
        result = qa_agent.answer_question(
            document_id=request.document_id,
            question=request.question
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process Q&A: {e}")
