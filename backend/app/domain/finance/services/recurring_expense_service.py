from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import HTTPException, status
from app.domain.finance.repositories.recurring_expense_repository import RecurringExpenseRepository
from app.domain.finance.repositories.category_repository import CategoryRepository
from app.domain.finance.repositories.transaction_repository import TransactionRepository
from app.domain.finance.dto.recurring_expense_dto import (
    RecurringExpenseCreate,
    RecurringExpenseUpdate,
    RecurringExpenseResponse,
    GenerateTransactionRequest
)
from app.domain.finance.dto.transaction_dto import TransactionResponse


class RecurringExpenseService:
    """Service for recurring expense operations"""
    
    def __init__(self):
        self.recurring_repository = RecurringExpenseRepository()
        self.category_repository = CategoryRepository()
        self.transaction_repository = TransactionRepository()
    
    async def create_recurring_expense(
        self,
        user_id: UUID,
        expense_data: RecurringExpenseCreate
    ) -> RecurringExpenseResponse:
        """Create a new recurring expense"""
        # Validate expense_type
        if expense_data.expense_type not in ['ongoing', 'installment']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expense type must be 'ongoing' or 'installment'"
            )
        
        # Validate day_of_month
        if not (1 <= expense_data.day_of_month <= 31):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Day of month must be between 1 and 31"
            )
        
        # Validate installment payments
        if expense_data.expense_type == 'installment':
            if expense_data.total_payments is None or expense_data.total_payments <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="total_payments is required for installment expenses and must be greater than 0"
                )
        else:
            # Ongoing expenses should not have total_payments
            if expense_data.total_payments is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="total_payments should not be set for ongoing expenses"
                )
        
        # Validate category exists and belongs to user
        category = await self.category_repository.find_by_user_and_id(user_id, expense_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
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
        
        expense = await self.recurring_repository.create(data)
        return RecurringExpenseResponse(**expense)
    
    async def get_recurring_expenses(
        self,
        user_id: UUID,
        is_active: Optional[bool] = None
    ) -> List[RecurringExpenseResponse]:
        """Get all recurring expenses for a user"""
        expenses = await self.recurring_repository.find_by_user_id(user_id, is_active)
        return [RecurringExpenseResponse(**exp) for exp in expenses]
    
    async def get_recurring_expense(
        self,
        user_id: UUID,
        expense_id: UUID
    ) -> RecurringExpenseResponse:
        """Get a recurring expense by ID"""
        expense = await self.recurring_repository.find_by_user_and_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring expense not found"
            )
        return RecurringExpenseResponse(**expense)
    
    async def update_recurring_expense(
        self,
        user_id: UUID,
        expense_id: UUID,
        expense_data: RecurringExpenseUpdate
    ) -> RecurringExpenseResponse:
        """Update a recurring expense"""
        # Verify expense exists and belongs to user
        expense = await self.recurring_repository.find_by_user_and_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring expense not found"
            )
        
        # Validate expense_type if provided
        if expense_data.expense_type and expense_data.expense_type not in ['ongoing', 'installment']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expense type must be 'ongoing' or 'installment'"
            )
        
        # Validate day_of_month if provided
        if expense_data.day_of_month is not None and not (1 <= expense_data.day_of_month <= 31):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Day of month must be between 1 and 31"
            )
        
        # Validate category if provided
        if expense_data.category_id:
            category = await self.category_repository.find_by_user_and_id(user_id, expense_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
        
        # Prepare update data
        update_data = {}
        if expense_data.name is not None:
            update_data["name"] = expense_data.name
        if expense_data.amount is not None:
            update_data["amount"] = expense_data.amount
        if expense_data.category_id is not None:
            update_data["category_id"] = expense_data.category_id
        if expense_data.day_of_month is not None:
            update_data["day_of_month"] = expense_data.day_of_month
        if expense_data.expense_type is not None:
            update_data["expense_type"] = expense_data.expense_type
        if expense_data.start_date is not None:
            update_data["start_date"] = expense_data.start_date
        if expense_data.total_payments is not None:
            update_data["total_payments"] = expense_data.total_payments
        if expense_data.is_active is not None:
            update_data["is_active"] = expense_data.is_active
        if expense_data.notes is not None:
            update_data["notes"] = expense_data.notes
        
        if not update_data:
            return RecurringExpenseResponse(**expense)
        
        updated_expense = await self.recurring_repository.update(expense_id, update_data)
        return RecurringExpenseResponse(**updated_expense)
    
    async def delete_recurring_expense(self, user_id: UUID, expense_id: UUID) -> bool:
        """Delete a recurring expense"""
        # Verify expense exists and belongs to user
        expense = await self.recurring_repository.find_by_user_and_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring expense not found"
            )
        
        return await self.recurring_repository.delete(expense_id)
    
    async def generate_transaction(
        self,
        user_id: UUID,
        expense_id: UUID,
        transaction_data: GenerateTransactionRequest
    ) -> TransactionResponse:
        """Generate a transaction from a recurring expense"""
        # Get recurring expense
        expense = await self.recurring_repository.find_by_user_and_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurring expense not found"
            )
        
        if not expense["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot generate transaction from inactive recurring expense"
            )
        
        # Create transaction
        from app.domain.finance.dto.transaction_dto import TransactionCreate
        transaction_create = TransactionCreate(
            date=transaction_data.date,
            amount=float(expense["amount"]) if expense["amount"] else 0.0,
            description=expense["name"],
            category_id=expense["category_id"],
            recurring_expense_id=expense_id,
            notes=transaction_data.notes or expense.get("notes")
        )
        
        transaction = await self.transaction_repository.create({
            "user_id": user_id,
            "date": transaction_create.date,
            "amount": transaction_create.amount,
            "description": transaction_create.description,
            "category_id": transaction_create.category_id,
            "recurring_expense_id": transaction_create.recurring_expense_id,
            "notes": transaction_create.notes
        })
        
        # Update payments_completed for installments
        if expense["expense_type"] == "installment":
            new_payments_completed = expense["payments_completed"] + 1
            update_data = {"payments_completed": new_payments_completed}
            
            # Auto-deactivate if all payments completed
            if expense["total_payments"] and new_payments_completed >= expense["total_payments"]:
                update_data["is_active"] = False
            
            await self.recurring_repository.update(expense_id, update_data)
        
        return TransactionResponse(**transaction)

