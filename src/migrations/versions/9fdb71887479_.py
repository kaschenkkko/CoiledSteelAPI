"""empty message

Revision ID: 9fdb71887479
Revises: 
Create Date: 2025-03-18 17:32:30.937824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fdb71887479'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coiled_steel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('length > 0', name='check_length_positive'),
    sa.CheckConstraint('weight > 0', name='check_weight_positive'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coiled_steel_id'), 'coiled_steel', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coiled_steel_id'), table_name='coiled_steel')
    op.drop_table('coiled_steel')
    # ### end Alembic commands ###
