from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy import select, and_
from app.core.repository import BaseRepository
from app.core.database import monthly_notes, get_db


class MonthlyNoteRepository(BaseRepository):
    """Repository for monthly note operations"""
    
    def __init__(self):
        super().__init__(monthly_notes)
    
    async def find_by_user_id(self, user_id: UUID, domain: str = "finance") -> List[Dict[str, Any]]:
        """Find all monthly notes for a user"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(
                and_(
                    self.table.c.user_id == user_id,
                    self.table.c.domain == domain
                )
            )
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_user_and_period(
        self, 
        user_id: UUID, 
        year: int, 
        month: int, 
        domain: str = "finance"
    ) -> Dict[str, Any] | None:
        """Find a monthly note by user ID, year, month, and domain"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(
                and_(
                    self.table.c.user_id == user_id,
                    self.table.c.domain == domain,
                    self.table.c.year == year,
                    self.table.c.month == month
                )
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def find_by_user_and_id(self, user_id: UUID, note_id: UUID) -> Dict[str, Any] | None:
        """Find a monthly note by user ID and note ID"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(
                and_(
                    self.table.c.user_id == user_id,
                    self.table.c.id == note_id
                )
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

