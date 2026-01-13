from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.finance.repositories.note_repository import NoteRepository
from app.domain.finance.dto.note_dto import (
    NoteCreate,
    NoteResponse
)
from app.domain.finance.validations.note_validations import validate_note_create


class NoteService:
    """Service for monthly and yearly note operations"""
    
    def __init__(self):
        self.note_repository = NoteRepository()
    
    async def create_or_update_note(
        self,
        user_id: UUID,
        note_data: NoteCreate
    ) -> NoteResponse:
        """Create or update a monthly or yearly note (creates if doesn't exist, updates if exists)"""
        # Validate note data
        validate_note_create(note_data)
        
        # Check if note already exists (excluding deleted)
        existing_note = await self.note_repository.find_by_user_and_period(
            user_id, note_data.year, note_data.month, note_data.domain, include_deleted=False
        )
        
        if existing_note:
            # Update existing note (only notes field can be updated)
            update_data = {"notes": note_data.notes}
            updated_note = await self.note_repository.update(existing_note["id"], update_data)
            return NoteResponse(**updated_note)
        else:
            # Create new note
            data = {
                "user_id": user_id,
                "domain": note_data.domain,
                "year": note_data.year,
                "month": note_data.month,  # Can be None for yearly notes
                "notes": note_data.notes
            }
            note = await self.note_repository.create(data)
            return NoteResponse(**note)
    
    async def get_notes(
        self,
        user_id: UUID,
        domain: str = "finance"
    ) -> List[NoteResponse]:
        """Get all monthly and yearly notes for a user"""
        notes = await self.note_repository.find_by_user_id(user_id, domain)
        return [NoteResponse(**note) for note in notes]
    
    async def get_note(
        self,
        user_id: UUID,
        year: int,
        month: Optional[int],
        domain: str = "finance"
    ) -> Optional[NoteResponse]:
        """Get a monthly or yearly note by year and month (month is None for yearly notes)"""
        note = await self.note_repository.find_by_user_and_period(user_id, year, month, domain)
        if not note:
            return None
        return NoteResponse(**note)
    
    async def delete_note(self, user_id: UUID, note_id: UUID) -> bool:
        """Soft delete a note"""
        # Verify note exists and belongs to user (exclude already deleted)
        note = await self.note_repository.find_by_user_and_id(user_id, note_id, include_deleted=False)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        
        return await self.note_repository.soft_delete(note_id)

