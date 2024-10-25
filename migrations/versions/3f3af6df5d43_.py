"""empty message

Revision ID: 3f3af6df5d43
Revises: 738d4efd5699
Create Date: 2024-10-18 11:37:31.536183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = '3f3af6df5d43'
down_revision: Union[str, None] = '738d4efd5699'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
