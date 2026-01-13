from fastapi import APIRouter, Query
from typing import List, Optional
from uuid import UUID
from datetime import date
from app.domain.finance.dto.transaction_dto import TransactionCreate, TransactionResponse
from app.domain.finance.services.transaction_service import TransactionService
from app.core.user_context import get_current_user_id

router = APIRouter()
transaction_service = TransactionService()


@router.post("", response_model=TransactionResponse, status_code=201)
async def create_transaction(transaction_data: TransactionCreate):
    """Create a new transaction"""
    user_id = get_current_user_id()
    return await transaction_service.create_transaction(user_id, transaction_data)


@router.get("", response_model=List[TransactionResponse])
async def get_transactions(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category_id: Optional[UUID] = Query(None),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(0),
):
    """Get all transactions for current user with optional filters"""
    user_id = get_current_user_id()
    return await transaction_service.get_transactions(
        user_id, start_date, end_date, category_id, limit, offset
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: UUID):
    """Get a transaction by ID"""
    user_id = get_current_user_id()
    return await transaction_service.get_transaction(user_id, transaction_id)


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: UUID):
    """Soft delete a transaction"""
    user_id = get_current_user_id()
    await transaction_service.delete_transaction(user_id, transaction_id)
    return None

