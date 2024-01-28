"""clear expense table v6

Revision ID: 331a19498818
Revises: 11789c5dda8c
Create Date: 2024-01-18 15:09:19.554305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "331a19498818"
down_revision: Union[str, None] = "11789c5dda8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DELETE FROM expense;")


def downgrade() -> None:
    pass
