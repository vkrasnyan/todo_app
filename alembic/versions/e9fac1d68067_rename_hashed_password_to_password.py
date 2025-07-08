"""Rename hashed_password to password

Revision ID: e9fac1d68067
Revises: 80b4c43284ec
Create Date: 2025-07-08 17:26:46.812633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e9fac1d68067'
down_revision: Union[str, None] = '80b4c43284ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "hashed_password", new_column_name="password")


def downgrade() -> None:
    op.alter_column("users", "password", new_column_name="hashed_password")