"""drop expense table

Revision ID: 805d84bbc3e5
Revises: 892c51dce165
Create Date: 2024-01-17 09:06:30.517776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '805d84bbc3e5'
down_revision: Union[str, None] = '892c51dce165'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
