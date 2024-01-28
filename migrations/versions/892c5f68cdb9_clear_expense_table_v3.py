"""clear expense table v3

Revision ID: 892c5f68cdb9
Revises: 872773f6b7ec
Create Date: 2024-01-18 09:16:54.610331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "892c5f68cdb9"
down_revision: Union[str, None] = "872773f6b7ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DELETE FROM expense;")


def downgrade() -> None:
    pass
