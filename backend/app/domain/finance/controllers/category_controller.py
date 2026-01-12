from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from app.domain.finance.dto.category_dto import CategoryCreate, CategoryUpdate, CategoryResponse
from app.domain.finance.services.category_service import CategoryService
from app.domain.auth.dto.auth_dto import UserResponse
from app.api.v1.auth import get_current_user

router = APIRouter()
category_service = CategoryService()


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_data: CategoryCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Create a new category"""
    return await category_service.create_category(current_user.id, category_data)


@router.get("", response_model=List[CategoryResponse])
async def get_categories(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get all categories for current user"""
    return await category_service.get_categories(current_user.id)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get a category by ID"""
    return await category_service.get_category(current_user.id, category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Update a category"""
    return await category_service.update_category(current_user.id, category_id, category_data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: UUID,
    current_user: UserResponse = Depends(get_current_user)
):
    """Delete a category"""
    await category_service.delete_category(current_user.id, category_id)
    return None

