"""sdffd

Revision ID: 83458db63104
Revises: 
Create Date: 2024-05-07 12:26:13.926057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83458db63104'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('status', sa.Enum('alive', 'dead', 'finished'), nullable=False),
    sa.Column('status_updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('last_message_sent', sa.TIMESTAMP(), nullable=False),
    sa.Column('current_stage', sa.Integer(), nullable=False),
    sa.Column('trigger', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###