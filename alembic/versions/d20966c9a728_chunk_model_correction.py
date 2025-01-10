"""Chunk model correction

Revision ID: d20966c9a728
Revises: 13cd495d6256
Create Date: 2024-12-28 01:28:57.486398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd20966c9a728'
down_revision: Union[str, None] = '13cd495d6256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chunks', 'serialized_text')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'chunks',
        sa.Column(
            'serialized_text',
            sa.TEXT(),
            autoincrement=False,
            nullable=False))
    # ### end Alembic commands ###
