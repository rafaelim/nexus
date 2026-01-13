"""add deleted_at to expenses

Revision ID: 003
Revises: 002
Create Date: 2024-01-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Add deleted_at column to expenses table
    op.add_column('expenses',
                  sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # Remove deleted_at column
    op.drop_column('expenses', 'deleted_at')

