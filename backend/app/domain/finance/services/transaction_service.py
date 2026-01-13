from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import HTTPException, status
from app.domain.finance.repositories.transaction_repository import TransactionRepository
from app.domain.finance.repositories.category_repository import CategoryRepository
from app.domain.finance.dto.transaction_dto import TransactionCreate, TransactionUpdate, TransactionResponse


class TransactionService:
    """Service for transaction operations"""
    
    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.category_repository = CategoryRepository()
    
    async def create_transaction(self, user_id: UUID, transaction_data: TransactionCreate) -> TransactionResponse:
        """Create a new transaction"""
        # Validate category exists and belongs to user
        category = await self.category_repository.find_by_user_and_id(user_id, transaction_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        # Validate expense_id if provided
        if transaction_data.expense_id:
            from app.domain.finance.repositories.expense_repository import ExpenseRepository
            expense_repo = ExpenseRepository()
            expense = await expense_repo.find_by_user_and_id(user_id, transaction_data.expense_id)
            if not expense:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Expense not found"
                )
        
        data = {
            "user_id": user_id,
            "date": transaction_data.date,
            "amount": transaction_data.amount,
            "description": transaction_data.description,
            "category_id": transaction_data.category_id,
            "expense_id": transaction_data.expense_id,
            "tags": transaction_data.tags,
            "payment_method": transaction_data.payment_method,
            "notes": transaction_data.notes
        }
        
        transaction = await self.transaction_repository.create(data)
        return TransactionResponse(**transaction)
    
    async def get_transactions(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category_id: Optional[UUID] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[TransactionResponse]:
        """Get all transactions for a user with optional filters"""
        transactions = await self.transaction_repository.find_by_user_id(
            user_id, start_date, end_date, category_id, limit, offset
        )
        return [TransactionResponse(**tx) for tx in transactions]
    
    async def get_transaction(self, user_id: UUID, transaction_id: UUID) -> TransactionResponse:
        """Get a transaction by ID"""
        transaction = await self.transaction_repository.find_by_user_and_id(user_id, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return TransactionResponse(**transaction)
    
    async def update_transaction(
        self,
        user_id: UUID,
        transaction_id: UUID,
        transaction_data: TransactionUpdate
    ) -> TransactionResponse:
        """Update a transaction"""
        # Verify transaction exists and belongs to user
        transaction = await self.transaction_repository.find_by_user_and_id(user_id, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Validate category if provided
        if transaction_data.category_id:
            category = await self.category_repository.find_by_user_and_id(user_id, transaction_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
        
        # Prepare update data
        update_data = {}
        if transaction_data.date is not None:
            update_data["date"] = transaction_data.date
        if transaction_data.amount is not None:
            update_data["amount"] = transaction_data.amount
        if transaction_data.description is not None:
            update_data["description"] = transaction_data.description
        if transaction_data.category_id is not None:
            update_data["category_id"] = transaction_data.category_id
        if transaction_data.tags is not None:
            update_data["tags"] = transaction_data.tags
        if transaction_data.payment_method is not None:
            update_data["payment_method"] = transaction_data.payment_method
        if transaction_data.notes is not None:
            update_data["notes"] = transaction_data.notes
        
        if not update_data:
            return TransactionResponse(**transaction)
        
        updated_transaction = await self.transaction_repository.update(transaction_id, update_data)
        return TransactionResponse(**updated_transaction)
    
    async def delete_transaction(self, user_id: UUID, transaction_id: UUID) -> bool:
        """Delete a transaction"""
        # Verify transaction exists and belongs to user
        transaction = await self.transaction_repository.find_by_user_and_id(user_id, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return await self.transaction_repository.delete(transaction_id)

