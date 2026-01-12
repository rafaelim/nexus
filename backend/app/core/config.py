from pydantic_settings import BaseSettings
from uuid import UUID


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Default User (for local development - no auth)
    DEFAULT_USER_ID: str = "00000000-0000-0000-0000-000000000001"  # Will be set after user creation
    
    # App
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


def get_default_user_id() -> UUID:
    """Get the default user ID for local development"""
    return UUID(settings.DEFAULT_USER_ID)

