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
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Find all transactions for a user with optional filters"""
        with self.db.connect() as conn:
            conditions = [self.table.c.user_id == user_id]
            
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
    
    async def find_by_user_and_id(self, user_id: UUID, transaction_id: UUID) -> Dict[str, Any] | None:
        """Find a transaction by user ID and transaction ID"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(
                (self.table.c.user_id == user_id) & 
                (self.table.c.id == transaction_id)
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

