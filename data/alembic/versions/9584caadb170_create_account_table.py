"""create account table

Revision ID: 9584caadb170
Revises:
Create Date: 2025-10-15 00:57:35.504030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9584caadb170'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('account')
