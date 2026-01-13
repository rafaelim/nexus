from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, datetime


class ExpenseCreate(BaseModel):
    name: str
    amount: Optional[float] = None
    category_id: UUID
    day_of_month: int
    expense_type: str  # 'ongoing' or 'installment'
    start_date: date
    total_payments: Optional[int] = None
    notes: Optional[str] = None


class ExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[UUID] = None
    day_of_month: Optional[int] = None
    expense_type: Optional[str] = None
    start_date: Optional[date] = None
    total_payments: Optional[int] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    amount: Optional[float]
    category_id: UUID
    day_of_month: int
    expense_type: str
    start_date: date
    total_payments: Optional[int]
    payments_completed: int
    is_active: bool
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GenerateTransactionRequest(BaseModel):
    date: date
    notes: Optional[str] = None

