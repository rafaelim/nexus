from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, and_
from app.core.repository import BaseRepository
from app.core.database import finance_categories, get_db


class CategoryRepository(BaseRepository):
    """Repository for category operations"""
    
    def __init__(self):
        super().__init__(finance_categories)
    
    async def find_by_user_id(self, user_id: UUID, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """Find all categories for a user (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [self.table.c.user_id == user_id]
            
            # Exclude deleted categories by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_user_and_id(self, user_id: UUID, category_id: UUID, include_deleted: bool = False) -> Dict[str, Any] | None:
        """Find a category by user ID and category ID (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.user_id == user_id,
                self.table.c.id == category_id
            ]
            
            # Exclude deleted categories by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def find_by_user_and_name(self, user_id: UUID, name: str, exclude_id: UUID | None = None) -> Dict[str, Any] | None:
        """Find a category by user ID and name (for uniqueness check, excludes deleted)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.user_id == user_id,
                self.table.c.name == name,
                self.table.c.deleted_at.is_(None)  # Only check active categories for uniqueness
            ]
            if exclude_id:
                conditions.append(self.table.c.id != exclude_id)
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def soft_delete(self, category_id: UUID) -> bool:
        """Soft delete a category by setting deleted_at timestamp"""
        with self.db.begin() as conn:
            stmt = self.table.update().where(
                self.table.c.id == category_id,
                self.table.c.deleted_at.is_(None)  # Only soft delete if not already deleted
            ).values(deleted_at=datetime.now(timezone.utc))
            result = conn.execute(stmt)
            return result.rowcount > 0

