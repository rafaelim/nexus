from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import HTTPException, status
from app.domain.finance.repositories.transaction_repository import TransactionRepository
from app.domain.finance.services.expense_service import ExpenseService
from app.domain.finance.dto.transaction_dto import TransactionCreate, TransactionResponse
from app.domain.finance.validations.transaction_validations import (
    validate_transaction_create,
    validate_property_exists
)


class TransactionService:
    """Service for transaction operations"""
    
    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.expense_service = ExpenseService()
    
    async def create_transaction(self, user_id: UUID, transaction_data: TransactionCreate) -> TransactionResponse:
        """Create a new transaction"""
        # Validate transaction data
        await validate_transaction_create(
            user_id,
            transaction_data.category_id,
            transaction_data.amount,
            transaction_data.property_id,
            transaction_data.expense_id
        )
        
        data = {
            "user_id": user_id,
            "house_id": transaction_data.house_id,
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
        
        # Update expense if linked
        if transaction_data.expense_id:
            await self.expense_service.record_payment(user_id, transaction_data.expense_id)
        
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
    
    async def delete_transaction(self, user_id: UUID, transaction_id: UUID) -> bool:
        """Soft delete a transaction"""
        # Verify transaction exists and belongs to user (exclude already deleted)
        transaction = await self.transaction_repository.find_by_user_and_id(user_id, transaction_id, include_deleted=False)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return await self.transaction_repository.soft_delete(transaction_id)

