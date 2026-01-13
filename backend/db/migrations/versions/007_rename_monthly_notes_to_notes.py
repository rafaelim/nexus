"""rename monthly_notes table to notes

Revision ID: 007
Revises: 006
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    # Rename the table
    op.rename_table('monthly_notes', 'notes')
    
    # Rename indexes
    op.execute('ALTER INDEX IF EXISTS idx_monthly_notes_user_id RENAME TO idx_notes_user_id')
    op.execute('ALTER INDEX IF EXISTS idx_monthly_notes_domain_year_month RENAME TO idx_notes_domain_year_month')
    op.execute('ALTER INDEX IF EXISTS uq_monthly_notes_user_domain_year_month RENAME TO uq_notes_user_domain_year_month')
    op.execute('ALTER INDEX IF EXISTS uq_monthly_notes_user_domain_year_yearly RENAME TO uq_notes_user_domain_year_yearly')


def downgrade():
    # Rename indexes back
    op.execute('ALTER INDEX IF EXISTS idx_notes_user_id RENAME TO idx_monthly_notes_user_id')
    op.execute('ALTER INDEX IF EXISTS idx_notes_domain_year_month RENAME TO idx_monthly_notes_domain_year_month')
    op.execute('ALTER INDEX IF EXISTS uq_notes_user_domain_year_month RENAME TO uq_monthly_notes_user_domain_year_month')
    op.execute('ALTER INDEX IF EXISTS uq_notes_user_domain_year_yearly RENAME TO uq_monthly_notes_user_domain_year_yearly')
    
    # Rename the table back
    op.rename_table('notes', 'monthly_notes')

