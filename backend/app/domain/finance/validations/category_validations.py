from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.domain.finance.dto.category_dto import CategoryCreate, CategoryUpdate
from app.domain.finance.repositories.category_repository import CategoryRepository
import re


def validate_category_type(category_type: str) -> None:
    """Validate that category_type is either 'income' or 'expense'"""
    if category_type not in ['income', 'expense']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category type must be 'income' or 'expense'"
        )


def validate_category_name(name: str) -> None:
    """Validate that category name is not empty"""
    if not name or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name is required and cannot be empty"
        )


def validate_category_color(color: Optional[str]) -> None:
    """Validate color format if provided (should be hex color code)"""
    if color is not None:
        # Hex color pattern: # followed by 6 hexadecimal digits
        hex_color_pattern = r'^#[0-9A-Fa-f]{6}$'
        if not re.match(hex_color_pattern, color):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Color must be a valid hex color code (e.g., '#FF5733')"
            )


def validate_category_create(category_data: CategoryCreate) -> None:
    """Composite validation for category creation"""
    validate_category_type(category_data.type)
    validate_category_name(category_data.name)
    validate_category_color(category_data.color)


async def validate_category_name_unique(user_id: UUID, name: str, exclude_id: Optional[UUID] = None) -> None:
    """Validate that category name is unique for the user (check for duplicates)"""
    category_repo = CategoryRepository()
    existing_category = await category_repo.find_by_user_and_name(user_id, name, exclude_id)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{name}' already exists for this user"
        )


def validate_category_update(category_data: CategoryUpdate) -> None:
    """Composite validation for category update (only validates provided fields)"""
    if category_data.type is not None:
        validate_category_type(category_data.type)
    
    if category_data.name is not None:
        validate_category_name(category_data.name)
    
    if category_data.color is not None:
        validate_category_color(category_data.color)

