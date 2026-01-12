from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime


class TransactionCreate(BaseModel):
    date: date
    amount: float
    description: Optional[str] = None
    category_id: UUID
    recurring_expense_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    amount: float
    description: Optional[str]
    category_id: UUID
    recurring_expense_id: Optional[UUID]
    tags: Optional[List[str]]
    payment_method: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

