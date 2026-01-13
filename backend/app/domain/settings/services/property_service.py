from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.domain.settings.dto.property_dto import PropertyCreate, PropertyUpdate, PropertyResponse
from app.domain.settings.repositories.property_repository import PropertyRepository
from app.domain.settings.validations.property_validations import (
    validate_property_create,
    validate_property_update,
    validate_property_exists,
    validate_property_name_unique,
)


class PropertyService:
    """Service for property operations"""
    
    def __init__(self):
        self.repository = PropertyRepository()
    
    async def create_property(self, property_data: PropertyCreate) -> PropertyResponse:
        """Create a new property"""
        # Validate property data
        validate_property_create(property_data)
        
        # Check for duplicate name
        await validate_property_name_unique(property_data.name)
        
        # Check if this is the first property (auto-set as default)
        all_properties = await self.repository.find_all()
        is_first_property = len(all_properties) == 0
        
        # Prepare property data
        property_dict = property_data.model_dump()
        if is_first_property:
            property_dict["is_default"] = True
        
        # Create property
        created_property = await self.repository.create_property(property_dict)
        
        # If setting as default, unset previous default (after creation)
        if created_property.get("is_default"):
            await self.repository.set_default_property(created_property["id"])
            # Refetch to get updated data
            created_property = await self.repository.find_by_id(created_property["id"])
        
        return PropertyResponse(**created_property)
    
    async def get_properties(self, include_deleted: bool = False) -> List[PropertyResponse]:
        """Get all properties (system-wide)"""
        properties = await self.repository.find_all(include_deleted)
        return [PropertyResponse(**property) for property in properties]
    
    async def get_property(self, property_id: UUID) -> PropertyResponse:
        """Get a specific property"""
        await validate_property_exists(property_id)
        property = await self.repository.find_by_id(property_id)
        if not property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        return PropertyResponse(**property)
    
    async def update_property(self, property_id: UUID, property_data: PropertyUpdate) -> PropertyResponse:
        """Update a property"""
        # Validate property exists
        await validate_property_exists(property_id)
        
        # Validate update data
        validate_property_update(property_data)
        
        # Check for duplicate name if name is being updated
        if property_data.name is not None:
            await validate_property_name_unique(property_data.name, exclude_id=property_id)
        
        # Prepare update data
        update_dict = property_data.model_dump(exclude_unset=True)
        
        # Handle default property logic
        if property_data.is_default is not None:
            if property_data.is_default:
                # Set this property as default (will unset previous default)
                await self.repository.set_default_property(property_id)
                # Remove is_default from update_dict since it's handled by set_default_property
                update_dict.pop("is_default", None)
            else:
                # Unset default - but we need to ensure at least one property is default
                current_property = await self.repository.find_by_id(property_id)
                if current_property and current_property.get("is_default"):
                    # Check if there are other properties
                    all_properties = await self.repository.find_all()
                    if len(all_properties) > 1:
                        # Find another property to set as default
                        other_properties = [p for p in all_properties if p["id"] != property_id]
                        if other_properties:
                            await self.repository.set_default_property(other_properties[0]["id"])
                    # If this is the only property, we can't unset default
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot unset default property. At least one property must be default."
                        )
        
        # Update property if there's anything to update
        if update_dict:
            updated_property = await self.repository.update_property(property_id, update_dict)
            if not updated_property:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Property not found"
                )
            return PropertyResponse(**updated_property)
        else:
            # If no update dict, just return the current property
            return await self.get_property(property_id)
    
    async def delete_property(self, property_id: UUID) -> None:
        """Soft delete a property"""
        await validate_property_exists(property_id)
        
        # Check if this is the default property
        property = await self.repository.find_by_id(property_id)
        if property and property.get("is_default"):
            # Check if there are other properties
            all_properties = await self.repository.find_all()
            other_properties = [p for p in all_properties if p["id"] != property_id]
            if other_properties:
                # Set another property as default
                await self.repository.set_default_property(other_properties[0]["id"])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot delete the only property. At least one property must exist."
                )
        
        deleted = await self.repository.soft_delete_property(property_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
    
    async def get_default_property(self) -> PropertyResponse | None:
        """Get default property (system-wide, helper method)"""
        default_property = await self.repository.get_default_property()
        if default_property:
            return PropertyResponse(**default_property)
        return None

