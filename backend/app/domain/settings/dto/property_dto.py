from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class PropertyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    is_active: Optional[bool] = Field(default=True)
    is_default: Optional[bool] = Field(default=False)


class PropertyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class PropertyResponse(BaseModel):
    id: UUID
    name: str
    is_active: bool
    is_default: bool
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

