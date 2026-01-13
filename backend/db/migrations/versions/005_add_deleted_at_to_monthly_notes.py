"""add deleted_at to monthly_notes

Revision ID: 005
Revises: 004
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # Add deleted_at column to monthly_notes
    op.add_column('monthly_notes', 
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():
    # Remove deleted_at column from monthly_notes
    op.drop_column('monthly_notes', 'deleted_at')
