"""clear expense table

Revision ID: 1eb8fb2d5c54
Revises: 805d84bbc3e5
Create Date: 2024-01-17 09:11:37.091014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1eb8fb2d5c54"
down_revision: Union[str, None] = "805d84bbc3e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DELETE FROM expense;")


def downgrade() -> None:
    pass
