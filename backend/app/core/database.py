from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, DateTime, DECIMAL, Boolean, Date, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.engine import Engine
from sqlalchemy.sql import func
import uuid
from app.core.config import settings

# Create engine
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
metadata = MetaData()

# Users table
users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String(255), unique=True, nullable=False),
    Column("first_name", String(255), nullable=False),
    Column("last_name", String(255), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# Finance categories table
finance_categories = Table(
    "finance_categories",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("name", String(255), nullable=False),
    Column("type", SQLEnum("income", "expense", name="category_type"), nullable=False),
    Column("color", String(7), nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# Expenses table
expenses = Table(
    "expenses",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("name", String(255), nullable=False),
    Column("amount", DECIMAL(10, 2), nullable=True),
    Column("category_id", UUID(as_uuid=True), ForeignKey("finance_categories.id"), nullable=False),
    Column("day_of_month", Integer, nullable=False),
    Column("expense_type", SQLEnum("ongoing", "installment", name="expense_type"), nullable=False),
    Column("start_date", Date, nullable=False),
    Column("total_payments", Integer, nullable=True),
    Column("payments_completed", Integer, default=0, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("notes", Text, nullable=True),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# Monthly notes table
monthly_notes = Table(
    "monthly_notes",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("domain", String(50), nullable=False, server_default="finance"),
    Column("year", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("notes", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# Finance transactions table
finance_transactions = Table(
    "finance_transactions",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("date", Date, nullable=False),
    Column("amount", DECIMAL(10, 2), nullable=False),
    Column("description", Text, nullable=True),
    Column("category_id", UUID(as_uuid=True), ForeignKey("finance_categories.id"), nullable=False),
    Column("expense_id", UUID(as_uuid=True), ForeignKey("expenses.id"), nullable=True),
    Column("tags", JSONB, nullable=True),
    Column("payment_method", String(100), nullable=True),
    Column("notes", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)


def get_db() -> Engine:
    """Get database engine"""
    return engine


def create_tables():
    """Create all tables"""
    metadata.create_all(engine)


def drop_tables():
    """Drop all tables"""
    metadata.drop_all(engine)

