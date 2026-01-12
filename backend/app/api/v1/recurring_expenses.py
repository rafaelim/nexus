from fastapi import APIRouter, Query
from typing import List, Optional
from uuid import UUID
from app.domain.finance.dto.recurring_expense_dto import (
    RecurringExpenseCreate,
    RecurringExpenseUpdate,
    RecurringExpenseResponse,
    GenerateTransactionRequest
)
from app.domain.finance.dto.transaction_dto import TransactionResponse
from app.domain.finance.services.recurring_expense_service import RecurringExpenseService
from app.core.user_context import get_current_user_id

router = APIRouter()
recurring_expense_service = RecurringExpenseService()


@router.post("", response_model=RecurringExpenseResponse, status_code=201)
async def create_recurring_expense(expense_data: RecurringExpenseCreate):
    """Create a new recurring expense"""
    user_id = get_current_user_id()
    return await recurring_expense_service.create_recurring_expense(user_id, expense_data)


@router.get("", response_model=List[RecurringExpenseResponse])
async def get_recurring_expenses(is_active: Optional[bool] = Query(None)):
    """Get all recurring expenses for current user"""
    user_id = get_current_user_id()
    return await recurring_expense_service.get_recurring_expenses(user_id, is_active)


@router.get("/{expense_id}", response_model=RecurringExpenseResponse)
async def get_recurring_expense(expense_id: UUID):
    """Get a recurring expense by ID"""
    user_id = get_current_user_id()
    return await recurring_expense_service.get_recurring_expense(user_id, expense_id)


@router.put("/{expense_id}", response_model=RecurringExpenseResponse)
async def update_recurring_expense(expense_id: UUID, expense_data: RecurringExpenseUpdate):
    """Update a recurring expense"""
    user_id = get_current_user_id()
    return await recurring_expense_service.update_recurring_expense(user_id, expense_id, expense_data)


@router.delete("/{expense_id}", status_code=204)
async def delete_recurring_expense(expense_id: UUID):
    """Delete a recurring expense"""
    user_id = get_current_user_id()
    await recurring_expense_service.delete_recurring_expense(user_id, expense_id)
    return None


@router.post("/{expense_id}/generate-transaction", response_model=TransactionResponse, status_code=201)
async def generate_transaction(expense_id: UUID, transaction_data: GenerateTransactionRequest):
    """Generate a transaction from a recurring expense"""
    user_id = get_current_user_id()
    return await recurring_expense_service.generate_transaction(user_id, expense_id, transaction_data)

