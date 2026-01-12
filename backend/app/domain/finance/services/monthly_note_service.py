from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.finance.repositories.monthly_note_repository import MonthlyNoteRepository
from app.domain.finance.dto.monthly_note_dto import (
    MonthlyNoteCreate,
    MonthlyNoteUpdate,
    MonthlyNoteResponse
)


class MonthlyNoteService:
    """Service for monthly note operations"""
    
    def __init__(self):
        self.note_repository = MonthlyNoteRepository()
    
    async def create_or_update_monthly_note(
        self,
        user_id: UUID,
        note_data: MonthlyNoteCreate
    ) -> MonthlyNoteResponse:
        """Create or update a monthly note"""
        # Validate month
        if not (1 <= note_data.month <= 12):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Month must be between 1 and 12"
            )
        
        # Check if note already exists
        existing_note = await self.note_repository.find_by_user_and_period(
            user_id, note_data.year, note_data.month, note_data.domain
        )
        
        if existing_note:
            # Update existing note
            update_data = {"notes": note_data.notes}
            updated_note = await self.note_repository.update(existing_note["id"], update_data)
            return MonthlyNoteResponse(**updated_note)
        else:
            # Create new note
            data = {
                "user_id": user_id,
                "domain": note_data.domain,
                "year": note_data.year,
                "month": note_data.month,
                "notes": note_data.notes
            }
            note = await self.note_repository.create(data)
            return MonthlyNoteResponse(**note)
    
    async def get_monthly_notes(
        self,
        user_id: UUID,
        domain: str = "finance"
    ) -> List[MonthlyNoteResponse]:
        """Get all monthly notes for a user"""
        notes = await self.note_repository.find_by_user_id(user_id, domain)
        return [MonthlyNoteResponse(**note) for note in notes]
    
    async def get_monthly_note(
        self,
        user_id: UUID,
        year: int,
        month: int,
        domain: str = "finance"
    ) -> Optional[MonthlyNoteResponse]:
        """Get a monthly note by year and month"""
        note = await self.note_repository.find_by_user_and_period(user_id, year, month, domain)
        if not note:
            return None
        return MonthlyNoteResponse(**note)
    
    async def update_monthly_note(
        self,
        user_id: UUID,
        note_id: UUID,
        note_data: MonthlyNoteUpdate
    ) -> MonthlyNoteResponse:
        """Update a monthly note"""
        # Verify note exists and belongs to user
        note = await self.note_repository.find_by_user_and_id(user_id, note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Monthly note not found"
            )
        
        # Prepare update data
        update_data = {}
        if note_data.notes is not None:
            update_data["notes"] = note_data.notes
        
        if not update_data:
            return MonthlyNoteResponse(**note)
        
        updated_note = await self.note_repository.update(note_id, update_data)
        return MonthlyNoteResponse(**updated_note)
    
    async def delete_monthly_note(self, user_id: UUID, note_id: UUID) -> bool:
        """Delete a monthly note"""
        # Verify note exists and belongs to user
        note = await self.note_repository.find_by_user_and_id(user_id, note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Monthly note not found"
            )
        
        return await self.note_repository.delete(note_id)

