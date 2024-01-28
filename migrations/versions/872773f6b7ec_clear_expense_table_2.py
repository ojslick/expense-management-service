"""clear expense table 2

Revision ID: 872773f6b7ec
Revises: 1eb8fb2d5c54
Create Date: 2024-01-17 09:29:12.143414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "872773f6b7ec"
down_revision: Union[str, None] = "1eb8fb2d5c54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DELETE FROM expense;")


def downgrade() -> None:
    pass
