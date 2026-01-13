from typing import List
from fastapi import APIRouter, HTTPException, status
from app.domain.settings.dto.property_dto import PropertyCreate, PropertyUpdate, PropertyResponse
from app.domain.settings.services.property_service import PropertyService

router = APIRouter(prefix="/properties", tags=["properties"])

property_service = PropertyService()


@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(property_data: PropertyCreate):
    """Create a new property"""
    return await property_service.create_property(property_data)


@router.get("", response_model=List[PropertyResponse])
async def get_properties(include_deleted: bool = False):
    """Get all properties (system-wide)"""
    return await property_service.get_properties(include_deleted)


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: str):
    """Get a specific property"""
    from uuid import UUID
    try:
        property_uuid = UUID(property_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid property ID format"
        )
    return await property_service.get_property(property_uuid)


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(property_id: str, property_data: PropertyUpdate):
    """Update a property"""
    from uuid import UUID
    try:
        property_uuid = UUID(property_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid property ID format"
        )
    return await property_service.update_property(property_uuid, property_data)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(property_id: str):
    """Soft delete a property"""
    from uuid import UUID
    try:
        property_uuid = UUID(property_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid property ID format"
        )
    await property_service.delete_property(property_uuid)
    return None

