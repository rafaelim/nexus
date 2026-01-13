"""add deleted_at to finance_transactions

Revision ID: 004
Revises: 003
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Add deleted_at column to finance_transactions
    op.add_column('finance_transactions', 
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():
    # Remove deleted_at column from finance_transactions
    op.drop_column('finance_transactions', 'deleted_at')

