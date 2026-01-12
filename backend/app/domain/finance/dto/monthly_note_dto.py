from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class MonthlyNoteCreate(BaseModel):
    domain: str = "finance"
    year: int
    month: int
    notes: str


class MonthlyNoteUpdate(BaseModel):
    notes: Optional[str] = None


class MonthlyNoteResponse(BaseModel):
    id: UUID
    user_id: UUID
    domain: str
    year: int
    month: int
    notes: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

