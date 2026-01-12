from fastapi import APIRouter, Query
from typing import List, Optional
from uuid import UUID
from app.domain.finance.dto.monthly_note_dto import (
    MonthlyNoteCreate,
    MonthlyNoteUpdate,
    MonthlyNoteResponse
)
from app.domain.finance.services.monthly_note_service import MonthlyNoteService
from app.core.user_context import get_current_user_id

router = APIRouter()
monthly_note_service = MonthlyNoteService()


@router.post("", response_model=MonthlyNoteResponse, status_code=201)
async def create_or_update_monthly_note(note_data: MonthlyNoteCreate):
    """Create or update a monthly note"""
    user_id = get_current_user_id()
    return await monthly_note_service.create_or_update_monthly_note(user_id, note_data)


@router.get("", response_model=List[MonthlyNoteResponse])
async def get_monthly_notes(domain: Optional[str] = Query("finance")):
    """Get all monthly notes for current user"""
    user_id = get_current_user_id()
    return await monthly_note_service.get_monthly_notes(user_id, domain)


@router.get("/{year}/{month}", response_model=Optional[MonthlyNoteResponse])
async def get_monthly_note(
    year: int,
    month: int,
    domain: Optional[str] = Query("finance")
):
    """Get a monthly note by year and month"""
    user_id = get_current_user_id()
    return await monthly_note_service.get_monthly_note(user_id, year, month, domain)


@router.put("/{note_id}", response_model=MonthlyNoteResponse)
async def update_monthly_note(note_id: UUID, note_data: MonthlyNoteUpdate):
    """Update a monthly note"""
    user_id = get_current_user_id()
    return await monthly_note_service.update_monthly_note(user_id, note_id, note_data)


@router.delete("/{note_id}", status_code=204)
async def delete_monthly_note(note_id: UUID):
    """Delete a monthly note"""
    user_id = get_current_user_id()
    await monthly_note_service.delete_monthly_note(user_id, note_id)
    return None

