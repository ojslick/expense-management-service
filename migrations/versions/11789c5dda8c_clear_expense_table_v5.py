"""clear expense table v5

Revision ID: 11789c5dda8c
Revises: 013cb369c64f
Create Date: 2024-01-18 15:08:31.548974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11789c5dda8c"
down_revision: Union[str, None] = "013cb369c64f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DELETE FROM expense;")


def downgrade() -> None:
    pass
