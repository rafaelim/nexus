from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class NoteCreate(BaseModel):
    domain: str = "finance"
    year: int
    month: Optional[int] = None  # None for yearly notes, 1-12 for monthly notes
    notes: str


class NoteResponse(BaseModel):
    id: UUID
    user_id: UUID
    domain: str
    year: int
    month: Optional[int]  # None for yearly notes, 1-12 for monthly notes
    notes: str
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

