"""Trying to create a new column for a table

Revision ID: 83ef3cad1438
Revises: 986a34715622
Create Date: 2025-12-22 19:17:45.723727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83ef3cad1438'
down_revision: Union[str, Sequence[str], None] = '986a34715622'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
