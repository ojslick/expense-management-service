"""clear expense table v4

Revision ID: 013cb369c64f
Revises: 892c5f68cdb9
Create Date: 2024-01-18 13:34:23.500332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "013cb369c64f"
down_revision: Union[str, None] = "892c5f68cdb9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DELETE FROM expense;")


def downgrade() -> None:
    pass
