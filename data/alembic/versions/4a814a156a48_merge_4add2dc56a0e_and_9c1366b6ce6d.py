"""merge 4add2dc56a0e and 9c1366b6ce6d

Revision ID: 4a814a156a48
Revises: 4add2dc56a0e, 9c1366b6ce6d
Create Date: 2025-11-02 17:26:48.057526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a814a156a48'
down_revision: Union[str, Sequence[str], None] = ('4add2dc56a0e', '9c1366b6ce6d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
