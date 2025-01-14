"""Add username

Revision ID: 323c50acfc27
Revises: 742fafaef582
Create Date: 2025-01-14 02:42:22.692404

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '323c50acfc27'
down_revision = '742fafaef582'
branch_labels = None
depends_on = None


def upgrade():
    # Add the column with a default value
    op.add_column('users', sa.Column('username', sa.String(),
                  nullable=False, server_default='default_username'))
    # Remove the default value constraint
    op.alter_column('users', 'username', server_default=None)


def downgrade():
    op.drop_column('users', 'username')
