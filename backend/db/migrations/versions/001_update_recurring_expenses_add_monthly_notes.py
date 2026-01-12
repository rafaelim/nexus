"""update recurring expenses add monthly notes

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Make amount nullable in recurring_expenses
    op.alter_column('recurring_expenses', 'amount',
                    existing_type=sa.DECIMAL(10, 2),
                    nullable=True)
    
    # Remove payment_method column from recurring_expenses
    op.drop_column('recurring_expenses', 'payment_method')
    
    # Create monthly_notes table
    op.create_table(
        'monthly_notes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('domain', sa.String(50), nullable=False, server_default='finance'),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'domain', 'year', 'month', name='uq_monthly_notes_user_domain_year_month')
    )
    
    # Create indexes
    op.create_index('idx_monthly_notes_user_id', 'monthly_notes', ['user_id'])
    op.create_index('idx_monthly_notes_domain_year_month', 'monthly_notes', ['domain', 'year', 'month'])


def downgrade():
    # Drop monthly_notes table and indexes
    op.drop_index('idx_monthly_notes_domain_year_month', table_name='monthly_notes')
    op.drop_index('idx_monthly_notes_user_id', table_name='monthly_notes')
    op.drop_table('monthly_notes')
    
    # Add payment_method column back
    op.add_column('recurring_expenses',
                  sa.Column('payment_method', sa.String(100), nullable=True))
    
    # Make amount NOT NULL again
    op.alter_column('recurring_expenses', 'amount',
                    existing_type=sa.DECIMAL(10, 2),
                    nullable=False)

