"""Add otp column to ProviderUser table

Revision ID: 738d4efd5699
Revises: d7215b4c1e43
Create Date: 2024-10-18 11:35:54.225255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = '738d4efd5699'
down_revision: Union[str, None] = 'd7215b4c1e43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ProviderUser', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.drop_column('ProviderUser', 'is_varified')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ProviderUser', sa.Column('is_varified', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('ProviderUser', 'is_verified')
    # ### end Alembic commands ###