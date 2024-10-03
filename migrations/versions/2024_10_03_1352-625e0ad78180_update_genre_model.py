"""Update Genre Model

Revision ID: 625e0ad78180
Revises: 92c655aa3b35
Create Date: 2024-10-03 13:52:58.854663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '625e0ad78180'
down_revision: Union[str, None] = '92c655aa3b35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genres', 'title',
               existing_type=postgresql.ENUM('ACTION', 'COMEDY', 'DRAMA', 'HORROR', 'FANTASY', 'SCI_FI', 'ROMANCE', 'THRILLER', 'DOCUMENTARY', 'ANIMATION', 'MYSTERY', 'ADVENTURE', 'FAMILY', 'CRIME', 'MUSICAL', 'HISTORICAL', name='genre'),
               type_=sa.String(length=30),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genres', 'title',
               existing_type=sa.String(length=30),
               type_=postgresql.ENUM('ACTION', 'COMEDY', 'DRAMA', 'HORROR', 'FANTASY', 'SCI_FI', 'ROMANCE', 'THRILLER', 'DOCUMENTARY', 'ANIMATION', 'MYSTERY', 'ADVENTURE', 'FAMILY', 'CRIME', 'MUSICAL', 'HISTORICAL', name='genre'),
               existing_nullable=False)
    # ### end Alembic commands ###
