"""add yearly notes support

Revision ID: 006
Revises: 005
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the existing unique constraint (check both possible names)
    try:
        op.drop_constraint('uq_monthly_notes_user_domain_year_month', 'monthly_notes', type_='unique')
    except:
        try:
            op.drop_constraint('monthly_notes_user_id_domain_year_month_key', 'monthly_notes', type_='unique')
        except:
            pass  # Constraint might not exist or have different name
    
    # Make month nullable
    op.alter_column('monthly_notes', 'month',
                    existing_type=sa.Integer(),
                    nullable=True)
    
    # Remove the CHECK constraint on month (we'll validate in application layer)
    op.drop_constraint('monthly_notes_month_check', 'monthly_notes', type_='check')
    
    # Create partial unique indexes for monthly and yearly notes
    # Monthly notes: unique on (user_id, domain, year, month) where month IS NOT NULL
    op.create_index(
        'uq_monthly_notes_user_domain_year_month',
        'monthly_notes',
        ['user_id', 'domain', 'year', 'month'],
        unique=True,
        postgresql_where=sa.text('month IS NOT NULL')
    )
    
    # Yearly notes: unique on (user_id, domain, year) where month IS NULL
    op.create_index(
        'uq_monthly_notes_user_domain_year_yearly',
        'monthly_notes',
        ['user_id', 'domain', 'year'],
        unique=True,
        postgresql_where=sa.text('month IS NULL')
    )


def downgrade():
    # Drop the partial unique indexes
    op.drop_index('uq_monthly_notes_user_domain_year_yearly', table_name='monthly_notes')
    op.drop_index('uq_monthly_notes_user_domain_year_month', table_name='monthly_notes')
    
    # Make month NOT NULL again
    op.alter_column('monthly_notes', 'month',
                    existing_type=sa.Integer(),
                    nullable=False)
    
    # Restore the CHECK constraint
    op.create_check_constraint(
        'monthly_notes_month_check',
        'monthly_notes',
        'month >= 1 AND month <= 12'
    )
    
    # Restore the original unique constraint
    op.create_unique_constraint(
        'monthly_notes_user_id_domain_year_month_key',
        'monthly_notes',
        ['user_id', 'domain', 'year', 'month']
    )

