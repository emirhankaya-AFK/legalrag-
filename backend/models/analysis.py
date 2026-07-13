from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalysisBase(BaseModel):
    document_id: int
    risk_score: int
    summary: Optional[str] = None
    risk_explanation: Optional[str] = None # JSON string
    analysis_date: Optional[str] = None

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: int

    class Config:
        from_attributes = True
