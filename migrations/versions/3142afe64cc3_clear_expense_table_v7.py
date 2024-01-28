"""clear expense table v7

Revision ID: 3142afe64cc3
Revises: 331a19498818
Create Date: 2024-01-19 08:45:29.442914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3142afe64cc3"
down_revision: Union[str, None] = "331a19498818"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DELETE FROM expense;")


def downgrade() -> None:
    pass
