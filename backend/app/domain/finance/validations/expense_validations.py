from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.finance.dto.expense_dto import ExpenseCreate, ExpenseUpdate
from app.domain.finance.repositories.category_repository import CategoryRepository
from app.domain.settings.repositories.property_repository import PropertyRepository


def validate_expense_type(expense_type: str) -> None:
    """Validate that expense_type is either 'ongoing' or 'installment'"""
    if expense_type not in ['ongoing', 'installment']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense type must be 'ongoing' or 'installment'"
        )


def validate_day_of_month(day_of_month: int) -> None:
    """Validate that day_of_month is between 1 and 31"""
    if not (1 <= day_of_month <= 31):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Day of month must be between 1 and 31"
        )


def validate_total_payments_for_installment(total_payments: Optional[int], expense_type: str) -> None:
    """Validate total_payments for installment expenses"""
    if expense_type == 'installment':
        if total_payments is None or total_payments <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="total_payments is required for installment expenses and must be greater than 0"
            )


def validate_total_payments_for_ongoing(total_payments: Optional[int], expense_type: str) -> None:
    """Validate that ongoing expenses don't have total_payments"""
    if expense_type == 'ongoing' and total_payments is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="total_payments should not be set for ongoing expenses"
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


async def validate_property_exists(property_id: UUID) -> None:
    """Validate that property exists (no user check needed, properties are system-wide)"""
    property_repo = PropertyRepository()
    property = await property_repo.find_by_id(property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )


def validate_expense_create(expense_data: ExpenseCreate) -> None:
    """Validate all fields for expense creation"""
    validate_expense_type(expense_data.expense_type)
    validate_day_of_month(expense_data.day_of_month)
    validate_total_payments_for_installment(expense_data.total_payments, expense_data.expense_type)
    validate_total_payments_for_ongoing(expense_data.total_payments, expense_data.expense_type)


def validate_total_payments_for_update(
    expense_data: ExpenseUpdate,
    current_expense_type: str
) -> None:
    """Validate total_payments for expense updates based on expense type"""
    # Only validate if expense_type or total_payments is being updated
    if expense_data.expense_type is None and expense_data.total_payments is None:
        return
    
    # Determine the new expense type (use updated value if provided, otherwise current)
    new_expense_type = expense_data.expense_type or current_expense_type
    
    # Validate total_payments if it's being set
    if expense_data.total_payments is not None:
        if new_expense_type == 'installment':
            if expense_data.total_payments <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="total_payments must be greater than 0 for installment expenses"
                )
        elif new_expense_type == 'ongoing':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="total_payments should not be set for ongoing expenses"
            )


def validate_expense_update(expense_data: ExpenseUpdate) -> None:
    """Validate fields for expense update (only validates provided fields)"""
    if expense_data.expense_type is not None:
        validate_expense_type(expense_data.expense_type)
    
    if expense_data.day_of_month is not None:
        validate_day_of_month(expense_data.day_of_month)

