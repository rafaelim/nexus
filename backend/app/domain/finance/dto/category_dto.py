from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    type: str  # 'income' or 'expense'
    color: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None


class CategoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    type: str
    color: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

