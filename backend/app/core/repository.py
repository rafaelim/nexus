from typing import Optional, List, Dict, Any
from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.engine import Engine
from uuid import UUID
from app.core.database import get_db


class BaseRepository:
    """Base repository class with common query methods"""
    
    def __init__(self, table, db: Engine = None):
        self.table = table
        self.db = db or get_db()
    
    async def find_by_id(self, id: UUID) -> Optional[Dict[str, Any]]:
        """Find a record by ID"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(self.table.c.id == id)
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def find_by(self, **filters) -> List[Dict[str, Any]]:
        """Find records by filters"""
        with self.db.connect() as conn:
            conditions = [getattr(self.table.c, key) == value for key, value in filters.items()]
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_one_by(self, **filters) -> Optional[Dict[str, Any]]:
        """Find one record by filters"""
        with self.db.connect() as conn:
            conditions = [getattr(self.table.c, key) == value for key, value in filters.items()]
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record"""
        with self.db.begin() as conn:
            stmt = insert(self.table).values(**data).returning(self.table)
            result = conn.execute(stmt)
            row = result.fetchone()
            return dict(row._mapping)
    
    async def update(self, id: UUID, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record by ID"""
        with self.db.begin() as conn:
            stmt = update(self.table).where(self.table.c.id == id).values(**data).returning(self.table)
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def delete(self, id: UUID) -> bool:
        """Delete a record by ID"""
        with self.db.begin() as conn:
            stmt = delete(self.table).where(self.table.c.id == id)
            result = conn.execute(stmt)
            return result.rowcount > 0
    
    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find all records with optional pagination"""
        with self.db.connect() as conn:
            stmt = select(self.table)
            if limit:
                stmt = stmt.limit(limit)
            if offset:
                stmt = stmt.offset(offset)
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]

