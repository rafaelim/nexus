from fastapi import APIRouter
from typing import List
from uuid import UUID
from app.domain.finance.dto.category_dto import CategoryCreate, CategoryUpdate, CategoryResponse
from app.domain.finance.services.category_service import CategoryService
from app.core.user_context import get_current_user_id

router = APIRouter()
category_service = CategoryService()


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(category_data: CategoryCreate):
    """Create a new category"""
    user_id = get_current_user_id()
    return await category_service.create_category(user_id, category_data)


@router.get("", response_model=List[CategoryResponse])
async def get_categories():
    """Get all categories for current user"""
    user_id = get_current_user_id()
    return await category_service.get_categories(user_id)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: UUID):
    """Get a category by ID"""
    user_id = get_current_user_id()
    return await category_service.get_category(user_id, category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: UUID, category_data: CategoryUpdate):
    """Update a category"""
    user_id = get_current_user_id()
    return await category_service.update_category(user_id, category_id, category_data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: UUID):
    """Delete a category"""
    user_id = get_current_user_id()
    await category_service.delete_category(user_id, category_id)
    return None

