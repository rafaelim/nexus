from typing import Optional, Dict, Any
from uuid import UUID
from app.core.repository import BaseRepository
from app.core.database import users


class UserRepository(BaseRepository):
    """Repository for user operations"""
    
    def __init__(self):
        super().__init__(users)
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find a user by email"""
        return await self.find_one_by(email=email)
    
    async def create_user(self, email: str, hashed_password: str) -> Dict[str, Any]:
        """Create a new user"""
        data = {
            "email": email,
            "hashed_password": hashed_password
        }
        return await self.create(data)

