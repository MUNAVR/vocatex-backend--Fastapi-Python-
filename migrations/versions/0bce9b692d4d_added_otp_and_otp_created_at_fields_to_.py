"""Added otp and otp_created_at fields to User

Revision ID: 0bce9b692d4d
Revises: b1844422ca6d
Create Date: 2024-10-16 09:47:54.328456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0bce9b692d4d'
down_revision: Union[str, None] = 'b1844422ca6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('otp', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('User', sa.Column('otp_created_at', postgresql.TIMESTAMP(), nullable=True))
    op.create_unique_constraint(None, 'resume_details', ['user_id'])
    op.drop_constraint('resume_details_user_id_fkey', 'resume_details', type_='foreignkey')
    op.create_foreign_key(None, 'resume_details', 'User', ['user_id'], ['uid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'resume_details', type_='foreignkey')
    op.create_foreign_key('resume_details_user_id_fkey', 'resume_details', 'User', ['user_id'], ['uid'])
    op.drop_constraint(None, 'resume_details', type_='unique')
    op.drop_column('User', 'otp_created_at')
    op.drop_column('User', 'otp')
    # ### end Alembic commands ###
