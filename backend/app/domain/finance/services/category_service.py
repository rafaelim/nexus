from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.finance.repositories.category_repository import CategoryRepository
from app.domain.finance.dto.category_dto import CategoryCreate, CategoryUpdate, CategoryResponse
from app.domain.finance.validations.category_validations import (
    validate_category_create,
    validate_category_update,
    validate_category_name_unique,
)


class CategoryService:
    """Service for category operations"""
    
    def __init__(self):
        self.category_repository = CategoryRepository()
    
    async def create_category(self, user_id: UUID, category_data: CategoryCreate) -> CategoryResponse:
        """Create a new category"""
        # Validate category data
        validate_category_create(category_data)
        
        # Check for duplicate name
        await validate_category_name_unique(user_id, category_data.name)
        
        data = {
            "user_id": user_id,
            "name": category_data.name,
            "type": category_data.type,
            "color": category_data.color
        }
        
        category = await self.category_repository.create(data)
        return CategoryResponse(**category)
    
    async def get_categories(self, user_id: UUID) -> List[CategoryResponse]:
        """Get all categories for a user"""
        categories = await self.category_repository.find_by_user_id(user_id)
        return [CategoryResponse(**cat) for cat in categories]
    
    async def get_category(self, user_id: UUID, category_id: UUID) -> CategoryResponse:
        """Get a category by ID"""
        category = await self.category_repository.find_by_user_and_id(user_id, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse(**category)
    
    async def update_category(self, user_id: UUID, category_id: UUID, category_data: CategoryUpdate) -> CategoryResponse:
        """Update a category"""
        # Verify category exists and belongs to user
        category = await self.category_repository.find_by_user_and_id(user_id, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        # Validate update data (only validates provided fields)
        validate_category_update(category_data)
        
        # Check for duplicate name if name is being updated
        if category_data.name is not None:
            await validate_category_name_unique(user_id, category_data.name, exclude_id=category_id)
        
        # Prepare update data - only include fields that were explicitly set
        update_data = category_data.model_dump(exclude_unset=True)
        
        if not update_data:
            return CategoryResponse(**category)
        
        updated_category = await self.category_repository.update(category_id, update_data)
        return CategoryResponse(**updated_category)
    
    async def delete_category(self, user_id: UUID, category_id: UUID) -> None:
        """Soft delete a category"""
        # Verify category exists and belongs to user
        category = await self.category_repository.find_by_user_and_id(user_id, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        deleted = await self.category_repository.soft_delete(category_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

