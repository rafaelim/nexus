from typing import Optional
from fastapi import HTTPException, status
from app.domain.finance.dto.note_dto import NoteCreate


def validate_month(month: Optional[int]) -> None:
    """Validate that month is between 1 and 12 if provided"""
    if month is not None:
        if not (1 <= month <= 12):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Month must be between 1 and 12"
            )


def validate_note_create(note_data: NoteCreate) -> None:
    """Validate all fields for note creation"""
    validate_month(note_data.month)

