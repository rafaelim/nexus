from fastapi import APIRouter, Query
from typing import List, Optional
from uuid import UUID
from app.domain.finance.dto.expense_dto import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    GenerateTransactionRequest
)
from app.domain.finance.dto.transaction_dto import TransactionResponse
from app.domain.finance.services.expense_service import ExpenseService
from app.core.user_context import get_current_user_id

router = APIRouter()
expense_service = ExpenseService()


@router.post("", response_model=ExpenseResponse, status_code=201)
async def create_expense(expense_data: ExpenseCreate):
    """Create a new expense"""
    user_id = get_current_user_id()
    return await expense_service.create_expense(user_id, expense_data)


@router.get("", response_model=List[ExpenseResponse])
async def get_expenses(is_active: Optional[bool] = Query(None)):
    """Get all expenses for current user"""
    user_id = get_current_user_id()
    return await expense_service.get_expenses(user_id, is_active)


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: UUID):
    """Get an expense by ID"""
    user_id = get_current_user_id()
    return await expense_service.get_expense(user_id, expense_id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(expense_id: UUID, expense_data: ExpenseUpdate):
    """Update an expense"""
    user_id = get_current_user_id()
    return await expense_service.update_expense(user_id, expense_id, expense_data)


@router.delete("/{expense_id}", status_code=204)
async def delete_expense(expense_id: UUID):
    """Delete an expense"""
    user_id = get_current_user_id()
    await expense_service.delete_expense(user_id, expense_id)
    return None


@router.post("/{expense_id}/generate-transaction", response_model=TransactionResponse, status_code=201)
async def generate_transaction(expense_id: UUID, transaction_data: GenerateTransactionRequest):
    """Generate a transaction from an expense"""
    user_id = get_current_user_id()
    return await expense_service.generate_transaction(user_id, expense_id, transaction_data)

