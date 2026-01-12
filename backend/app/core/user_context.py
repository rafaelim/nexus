from uuid import UUID
from app.core.config import get_default_user_id


def get_current_user_id() -> UUID:
    """Get the current user ID - for local development, returns default user"""
    return get_default_user_id()

