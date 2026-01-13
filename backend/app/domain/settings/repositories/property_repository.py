from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, and_, update, insert
from app.core.repository import BaseRepository
from app.core.database import properties, get_db


class PropertyRepository(BaseRepository):
    """Repository for property operations"""
    
    def __init__(self):
        super().__init__(properties)
    
    async def find_all(self, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """Find all properties (system-wide, not user-scoped)"""
        with self.db.connect() as conn:
            conditions = []
            
            # Exclude deleted properties by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table)
            if conditions:
                stmt = stmt.where(and_(*conditions))
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result.fetchall()]
    
    async def find_by_id(self, property_id: UUID, include_deleted: bool = False) -> Optional[Dict[str, Any]]:
        """Find a property by ID (excludes deleted by default)"""
        with self.db.connect() as conn:
            conditions = [self.table.c.id == property_id]
            
            # Exclude deleted properties by default
            if not include_deleted:
                conditions.append(self.table.c.deleted_at.is_(None))
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def create_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new property"""
        with self.db.begin() as conn:
            stmt = insert(self.table).values(**property_data).returning(self.table)
            result = conn.execute(stmt)
            row = result.fetchone()
            return dict(row._mapping)
    
    async def update_property(self, property_id: UUID, property_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a property"""
        with self.db.begin() as conn:
            stmt = update(self.table).where(
                self.table.c.id == property_id,
                self.table.c.deleted_at.is_(None)
            ).values(**property_data).returning(self.table)
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def soft_delete_property(self, property_id: UUID) -> bool:
        """Soft delete a property"""
        with self.db.begin() as conn:
            stmt = update(self.table).where(
                self.table.c.id == property_id,
                self.table.c.deleted_at.is_(None)
            ).values(deleted_at=datetime.now(timezone.utc))
            result = conn.execute(stmt)
            return result.rowcount > 0
    
    async def get_default_property(self) -> Optional[Dict[str, Any]]:
        """Get the default property (system-wide)"""
        with self.db.connect() as conn:
            stmt = select(self.table).where(
                self.table.c.is_default == True,
                self.table.c.deleted_at.is_(None)
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
    
    async def set_default_property(self, property_id: UUID) -> bool:
        """Set a property as default (unsets previous default)"""
        with self.db.begin() as conn:
            # First, unset all default properties
            unset_stmt = update(self.table).where(
                self.table.c.is_default == True,
                self.table.c.deleted_at.is_(None)
            ).values(is_default=False)
            conn.execute(unset_stmt)
            
            # Then set the new default
            set_stmt = update(self.table).where(
                self.table.c.id == property_id,
                self.table.c.deleted_at.is_(None)
            ).values(is_default=True)
            result = conn.execute(set_stmt)
            return result.rowcount > 0
    
    async def find_by_name(self, name: str, exclude_id: Optional[UUID] = None) -> Optional[Dict[str, Any]]:
        """Find a property by name (for uniqueness check)"""
        with self.db.connect() as conn:
            conditions = [
                self.table.c.name == name,
                self.table.c.deleted_at.is_(None)
            ]
            if exclude_id:
                conditions.append(self.table.c.id != exclude_id)
            
            stmt = select(self.table).where(and_(*conditions))
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

