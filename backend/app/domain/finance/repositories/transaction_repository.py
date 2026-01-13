from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import date
from sqlalchemy import select, and_, or_, desc
from app.core.repository import BaseRepository
from app.core.database import finance_transactions, get_db


class TransactionRepository(BaseRepository):
    """Repository for transaction operations"""
    
    def __init__(self):
        super().__init__(finance_transactions)
    
    async def find_by_user_id(
        self, 
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category_id: Optional[UUID] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        include_deleted: bool = False
    ) -> List[Dict[str, Any]]:
        """Find all transactions for a user with optional filters (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [self.table.c.user_id == user_id]
            
            # Exclude deleted transactions by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            if start_date:
                conditions.append(self.table.c.date >= start_date)
            if end_date:
                conditions.append(self.table.c.date <= end_date)
            if category_id:
                conditions.append(self.table.c.category_id == category_id)
            
            stmt = select(self.table).where(and_(*conditions)).order_by(desc(self.table.c.date))
            
            if limit:
                stmt = stmt.limit(limit)
            if offset:
                stmt = stmt.offset(offset)
            
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_user_and_id(self, user_id: UUID, transaction_id: UUID, include_deleted: bool = False) -> Dict[str, Any] | None:
        """Find a transaction by user ID and transaction ID (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.user_id == user_id,
                self.table.c.id == transaction_id
            ]
            
            # Exclude deleted transactions by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def soft_delete(self, transaction_id: UUID) -> bool:
        """Soft delete a transaction by setting deleted_at timestamp"""
        from datetime import datetime, timezone
        with self.db.connect() as conn:
            update_stmt = (
                self.table.update()
                .where(self.table.c.id == transaction_id)
                .values(deleted_at=datetime.now(timezone.utc))
            )
            result = conn.execute(update_stmt)
            conn.commit()
            return result.rowcount > 0

