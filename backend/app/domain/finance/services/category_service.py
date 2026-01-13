from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.finance.repositories.category_repository import CategoryRepository
from app.domain.finance.dto.category_dto import CategoryCreate, CategoryUpdate, CategoryResponse


class CategoryService:
    """Service for category operations"""
    
    def __init__(self):
        self.category_repository = CategoryRepository()
    
    async def create_category(self, user_id: UUID, category_data: CategoryCreate) -> CategoryResponse:
        """Create a new category"""
        # Validate type
        if category_data.type not in ['income', 'expense']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type must be 'income' or 'expense'"
            )
        
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
        
        # Validate type if provided
        if category_data.type and category_data.type not in ['income', 'expense']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type must be 'income' or 'expense'"
            )
        
        # Prepare update data - only include fields that were explicitly set
        update_data = category_data.model_dump(exclude_unset=True)
        
        if not update_data:
            return CategoryResponse(**category)
        
        updated_category = await self.category_repository.update(category_id, update_data)
        return CategoryResponse(**updated_category)
    
    async def delete_category(self, user_id: UUID, category_id: UUID) -> bool:
        """Delete a category"""
        # Verify category exists and belongs to user
        category = await self.category_repository.find_by_user_and_id(user_id, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        return await self.category_repository.delete(category_id)

