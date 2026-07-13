from pydantic import BaseModel
from typing import Optional

class ClauseBase(BaseModel):
    document_id: int
    clause_type: str
    content: str
    risk_level: str
    page_num: Optional[int] = None

class ClauseCreate(ClauseBase):
    pass

class Clause(ClauseBase):
    id: int

    class Config:
        from_attributes = True
