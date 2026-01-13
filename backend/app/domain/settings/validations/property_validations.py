from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.settings.dto.property_dto import PropertyCreate, PropertyUpdate
from app.domain.settings.repositories.property_repository import PropertyRepository


def validate_property_name(name: str) -> None:
    """Validate that property name is not empty"""
    if not name or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Property name is required and cannot be empty"
        )


async def validate_property_exists(property_id: UUID) -> None:
    """Validate that property exists (no user check needed, properties are system-wide)"""
    property_repo = PropertyRepository()
    property = await property_repo.find_by_id(property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )


async def validate_property_name_unique(name: str, exclude_id: Optional[UUID] = None) -> None:
    """Validate that property name is unique (check for duplicates)"""
    property_repo = PropertyRepository()
    existing_property = await property_repo.find_by_name(name, exclude_id)
    if existing_property:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Property with name '{name}' already exists"
        )


def validate_property_create(property_data: PropertyCreate) -> None:
    """Composite validation for property creation"""
    validate_property_name(property_data.name)


def validate_property_update(property_data: PropertyUpdate) -> None:
    """Composite validation for property update"""
    if property_data.name is not None:
        validate_property_name(property_data.name)

