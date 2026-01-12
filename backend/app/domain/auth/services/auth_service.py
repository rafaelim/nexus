from typing import Optional
from datetime import timedelta
from app.domain.auth.repositories.user_repository import UserRepository
from app.domain.auth.dto.auth_dto import UserCreate, UserResponse, TokenResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from fastapi import HTTPException, status


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    async def register(self, user_data: UserCreate) -> TokenResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.user_repository.find_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = await self.user_repository.create_user(user_data.email, hashed_password)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user["id"])},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(**user)
        )
    
    async def login(self, email: str, password: str) -> TokenResponse:
        """Authenticate user and return token"""
        # Find user
        user = await self.user_repository.find_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user["id"])},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(**user)
        )
    
    async def get_current_user(self, user_id: str) -> Optional[UserResponse]:
        """Get current user by ID"""
        from uuid import UUID
        user = await self.user_repository.find_by_id(UUID(user_id))
        if not user:
            return None
        return UserResponse(**user)

