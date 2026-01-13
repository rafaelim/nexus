from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy import select, and_
from app.core.repository import BaseRepository
from app.core.database import expenses, get_db


class ExpenseRepository(BaseRepository):
    """Repository for expense operations"""
    
    def __init__(self):
        super().__init__(expenses)
    
    async def find_by_user_id(self, user_id: UUID, is_active: bool = None) -> List[Dict[str, Any]]:
        """Find all expenses for a user"""
        with self.db.connect() as conn:
            conditions = [self.table.c.user_id == user_id]
            if is_active is not None:
                conditions.append(self.table.c.is_active == is_active)
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_user_and_id(self, user_id: UUID, expense_id: UUID) -> Dict[str, Any] | None:
        """Find an expense by user ID and expense ID"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(
                (self.table.c.user_id == user_id) & 
                (self.table.c.id == expense_id)
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

