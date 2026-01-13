from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, and_, or_
from app.core.repository import BaseRepository
from app.core.database import expenses, get_db


class ExpenseRepository(BaseRepository):
    """Repository for expense operations"""
    
    def __init__(self):
        super().__init__(expenses)
    
    async def find_by_user_id(self, user_id: UUID, is_active: bool = None, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """Find all expenses for a user (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [self.table.c.user_id == user_id]
            
            # Exclude deleted expenses by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            if is_active is not None:
                conditions.append(self.table.c.is_active == is_active)
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_user_and_id(self, user_id: UUID, expense_id: UUID, include_deleted: bool = False) -> Dict[str, Any] | None:
        """Find an expense by user ID and expense ID (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.user_id == user_id,
                self.table.c.id == expense_id
            ]
            
            # Exclude deleted expenses by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def soft_delete(self, expense_id: UUID) -> bool:
        """Soft delete an expense by setting deleted_at timestamp"""
        with self.db.connect() as conn:
            stmt = self.table.update().where(
                self.table.c.id == expense_id
            ).values(deleted_at=datetime.now(timezone.utc))
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0

