from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import HTTPException, status
from app.domain.finance.repositories.expense_repository import ExpenseRepository
from app.domain.finance.repositories.category_repository import CategoryRepository
from app.domain.finance.repositories.transaction_repository import TransactionRepository
from app.domain.finance.dto.expense_dto import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse
)
from app.domain.finance.validations.expense_validations import (
    validate_expense_create,
    validate_expense_update,
    validate_category_exists,
    validate_total_payments_for_update
)


class ExpenseService:
    """Service for expense operations"""
    
    def __init__(self):
        self.expense_repository = ExpenseRepository()
        self.category_repository = CategoryRepository()
        self.transaction_repository = TransactionRepository()
    
    async def create_expense(
        self,
        user_id: UUID,
        expense_data: ExpenseCreate
    ) -> ExpenseResponse:
        """Create a new expense"""
        # Validate expense data
        validate_expense_create(expense_data)
        await validate_category_exists(user_id, expense_data.category_id)
        
        data = {
            "user_id": user_id,
            "name": expense_data.name,
            "amount": expense_data.amount,
            "category_id": expense_data.category_id,
            "day_of_month": expense_data.day_of_month,
            "expense_type": expense_data.expense_type,
            "start_date": expense_data.start_date,
            "total_payments": expense_data.total_payments,
            "payments_completed": 0,
            "is_active": True,
            "notes": expense_data.notes
        }
        
        expense = await self.expense_repository.create(data)
        return ExpenseResponse(**expense)
    
    async def get_expenses(
        self,
        user_id: UUID,
        is_active: Optional[bool] = None
    ) -> List[ExpenseResponse]:
        """Get all expenses for a user"""
        expenses = await self.expense_repository.find_by_user_id(user_id, is_active)
        return [ExpenseResponse(**exp) for exp in expenses]
    
    async def get_expense(
        self,
        user_id: UUID,
        expense_id: UUID
    ) -> ExpenseResponse:
        """Get an expense by ID"""
        expense = await self.expense_repository.find_by_user_and_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        return ExpenseResponse(**expense)
    
    async def update_expense(
        self,
        user_id: UUID,
        expense_id: UUID,
        expense_data: ExpenseUpdate
    ) -> ExpenseResponse:
        """Update an expense"""
        # Verify expense exists and belongs to user
        expense = await self.expense_repository.find_by_user_and_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        # Validate expense data (only validates provided fields)
        validate_expense_update(expense_data)
        
        # Validate category if provided
        if expense_data.category_id:
            await validate_category_exists(user_id, expense_data.category_id)
        
        # Validate total_payments based on expense type (current or updated)
        validate_total_payments_for_update(expense_data, expense["expense_type"])
        
        # Prepare update data - only include fields that were explicitly set
        update_data = expense_data.model_dump(exclude_unset=True)
        
        if not update_data:
            return ExpenseResponse(**expense)
        
        updated_expense = await self.expense_repository.update(expense_id, update_data)
        return ExpenseResponse(**updated_expense)
    
    async def delete_expense(self, user_id: UUID, expense_id: UUID) -> bool:
        """Soft delete an expense"""
        # Verify expense exists and belongs to user (exclude already deleted)
        expense = await self.expense_repository.find_by_user_and_id(user_id, expense_id, include_deleted=False)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        return await self.expense_repository.soft_delete(expense_id)
    
    async def record_payment(self, user_id: UUID, expense_id: UUID) -> None:
        """Record a payment for an expense (increment payments_completed for installments)"""
        # Get expense and verify it belongs to user
        expense = await self.expense_repository.find_by_user_and_id(user_id, expense_id, include_deleted=False)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        # Update payments_completed for installments
        if expense["expense_type"] == "installment":
            new_payments_completed = expense["payments_completed"] + 1
            update_data = {"payments_completed": new_payments_completed}
            
            # Auto-deactivate if all payments completed
            if expense["total_payments"] and new_payments_completed >= expense["total_payments"]:
                update_data["is_active"] = False
            
            await self.expense_repository.update(expense_id, update_data)
        # For ongoing expenses, no update needed
    

