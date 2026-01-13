"""rename recurring_expenses to expenses

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Rename the table
    op.rename_table('recurring_expenses', 'expenses')
    
    # Rename indexes
    op.execute('ALTER INDEX IF EXISTS idx_recurring_expenses_user_id RENAME TO idx_expenses_user_id')
    op.execute('ALTER INDEX IF EXISTS idx_recurring_expenses_category_id RENAME TO idx_expenses_category_id')
    
    # Rename foreign key column in finance_transactions
    op.alter_column('finance_transactions', 'recurring_expense_id',
                    new_column_name='expense_id',
                    existing_type=postgresql.UUID(as_uuid=True),
                    nullable=True)
    
    # Drop old foreign key constraint and create new one
    op.drop_constraint('finance_transactions_recurring_expense_id_fkey', 'finance_transactions', type_='foreignkey')
    op.create_foreign_key('finance_transactions_expense_id_fkey', 'finance_transactions', 'expenses', ['expense_id'], ['id'], ondelete='SET NULL')
    
    # Rename index for the foreign key
    op.execute('ALTER INDEX IF EXISTS idx_finance_transactions_recurring_expense_id RENAME TO idx_finance_transactions_expense_id')


def downgrade():
    # Rename index back
    op.execute('ALTER INDEX IF EXISTS idx_finance_transactions_expense_id RENAME TO idx_finance_transactions_recurring_expense_id')
    
    # Drop new foreign key and recreate old one
    op.drop_constraint('finance_transactions_expense_id_fkey', 'finance_transactions', type_='foreignkey')
    op.create_foreign_key('finance_transactions_recurring_expense_id_fkey', 'finance_transactions', 'recurring_expenses', ['expense_id'], ['id'], ondelete='SET NULL')
    
    # Rename foreign key column back
    op.alter_column('finance_transactions', 'expense_id',
                    new_column_name='recurring_expense_id',
                    existing_type=postgresql.UUID(as_uuid=True),
                    nullable=True)
    
    # Rename indexes back
    op.execute('ALTER INDEX IF EXISTS idx_expenses_category_id RENAME TO idx_recurring_expenses_category_id')
    op.execute('ALTER INDEX IF EXISTS idx_expenses_user_id RENAME TO idx_recurring_expenses_user_id')
    
    # Rename the table back
    op.rename_table('expenses', 'recurring_expenses')

