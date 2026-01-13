from fastapi import APIRouter, Query
from typing import List, Optional
from uuid import UUID
from app.domain.finance.dto.note_dto import (
    NoteCreate,
    NoteResponse
)
from app.domain.finance.services.note_service import NoteService
from app.core.user_context import get_current_user_id

router = APIRouter()
note_service = NoteService()


@router.post("", response_model=NoteResponse, status_code=201)
async def create_or_update_note(note_data: NoteCreate):
    """Create or update a monthly or yearly note (month is optional - omit for yearly notes)"""
    user_id = get_current_user_id()
    return await note_service.create_or_update_note(user_id, note_data)


@router.get("", response_model=List[NoteResponse])
async def get_notes(domain: Optional[str] = Query("finance")):
    """Get all monthly and yearly notes for current user"""
    user_id = get_current_user_id()
    return await note_service.get_notes(user_id, domain)


@router.get("/year/{year}", response_model=Optional[NoteResponse])
async def get_yearly_note(
    year: int,
    domain: Optional[str] = Query("finance")
):
    """Get a yearly note by year (month is None)"""
    user_id = get_current_user_id()
    return await note_service.get_note(user_id, year, None, domain)


@router.get("/year/{year}/month/{month}", response_model=Optional[NoteResponse])
async def get_monthly_note(
    year: int,
    month: int,
    domain: Optional[str] = Query("finance")
):
    """Get a monthly note by year and month"""
    user_id = get_current_user_id()
    return await note_service.get_note(user_id, year, month, domain)


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: UUID):
    """Soft delete a note"""
    user_id = get_current_user_id()
    await note_service.delete_note(user_id, note_id)
    return None

