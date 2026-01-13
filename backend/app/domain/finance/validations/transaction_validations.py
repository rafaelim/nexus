from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.finance.repositories.category_repository import CategoryRepository
from app.domain.finance.services.expense_service import ExpenseService


def validate_amount(amount: float) -> None:
    """Validate that amount is greater than 0"""
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )


async def validate_category_exists(user_id: UUID, category_id: UUID) -> None:
    """Validate that category exists and belongs to user"""
    category_repo = CategoryRepository()
    category = await category_repo.find_by_user_and_id(user_id, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )


async def validate_expense_exists(user_id: UUID, expense_id: UUID) -> None:
    """Validate that expense exists and belongs to user"""
    expense_service = ExpenseService()
    try:
        await expense_service.get_expense(user_id, expense_id)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )


async def validate_transaction_create(user_id: UUID, category_id: UUID, amount: float, expense_id: Optional[UUID] = None) -> None:
    """Validate all fields for transaction creation"""
    validate_amount(amount)
    await validate_category_exists(user_id, category_id)
    if expense_id:
        await validate_expense_exists(user_id, expense_id)

