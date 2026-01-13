from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy import select, and_
from app.core.repository import BaseRepository
from app.core.database import notes, get_db


class NoteRepository(BaseRepository):
    """Repository for monthly and yearly note operations"""
    
    def __init__(self):
        super().__init__(notes)
    
    async def find_by_user_id(self, user_id: UUID, domain: str = "finance", include_deleted: bool = False) -> List[Dict[str, Any]]:
        """Find all monthly and yearly notes for a user (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.user_id == user_id,
                self.table.c.domain == domain
            ]
            
            # Exclude deleted notes by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_user_and_period(
        self, 
        user_id: UUID, 
        year: int, 
        month: Optional[int], 
        domain: str = "finance",
        include_deleted: bool = False
    ) -> Dict[str, Any] | None:
        """Find a monthly or yearly note by user ID, year, month (optional), and domain (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.user_id == user_id,
                self.table.c.domain == domain,
                self.table.c.year == year
            ]
            
            # For monthly notes, match month; for yearly notes, month must be NULL
            if month is not None:
                conditions.append(self.table.c.month == month)
            else:
                conditions.append(self.table.c.month.is_(None))
            
            # Exclude deleted notes by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def find_by_user_and_id(self, user_id: UUID, note_id: UUID, include_deleted: bool = False) -> Dict[str, Any] | None:
        """Find a note by user ID and note ID (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.user_id == user_id,
                self.table.c.id == note_id
            ]
            
            # Exclude deleted notes by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def soft_delete(self, note_id: UUID) -> bool:
        """Soft delete a note by setting deleted_at timestamp"""
        from datetime import datetime, timezone
        with self.db.connect() as conn:
            update_stmt = (
                self.table.update()
                .where(self.table.c.id == note_id)
                .values(deleted_at=datetime.now(timezone.utc))
            )
            result = conn.execute(update_stmt)
            conn.commit()
            return result.rowcount > 0

