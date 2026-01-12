from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.auth.dto.auth_dto import UserCreate, UserResponse, TokenResponse, LoginRequest
from app.domain.auth.services.auth_service import AuthService
from app.core.security import decode_access_token
from typing import Optional


router = APIRouter()
auth_service = AuthService()


def get_current_user_id(token: str = Depends(lambda: None)) -> Optional[str]:
    """Dependency to get current user ID from token"""
    # This is a simplified version - in production, use proper dependency injection
    # For now, we'll handle auth in the routes
    return None


async def get_current_user(token: str) -> Optional[UserResponse]:
    """Get current authenticated user"""
    payload = decode_access_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    return await auth_service.get_current_user(user_id)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    return await auth_service.register(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Login user"""
    return await auth_service.login(login_data.email, login_data.password)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return current_user

