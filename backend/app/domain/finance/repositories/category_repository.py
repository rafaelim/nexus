from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy import select
from app.core.repository import BaseRepository
from app.core.database import finance_categories, get_db


class CategoryRepository(BaseRepository):
    """Repository for category operations"""
    
    def __init__(self):
        super().__init__(finance_categories)
    
    async def find_by_user_id(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Find all categories for a user"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(self.table.c.user_id == user_id)
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_user_and_id(self, user_id: UUID, category_id: UUID) -> Dict[str, Any] | None:
        """Find a category by user ID and category ID"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(
                (self.table.c.user_id == user_id) & 
                (self.table.c.id == category_id)
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

