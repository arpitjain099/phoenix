"""Description to name gather.

Revision ID: 7913f5e9f28c
Revises: 372dbf7eea43
Create Date: 2024-07-09 08:31:15.296606

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "7913f5e9f28c"
down_revision: Union[str, None] = "372dbf7eea43"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade for 7913f5e9f28c."""
    # Add the new 'name' column
    op.add_column("gathers", sa.Column("name", sa.String(), nullable=True))

    # Copy data from 'description' to 'name'
    op.execute("UPDATE gathers SET name = description")

    # Make the 'name' column non-nullable
    op.alter_column("gathers", "name", nullable=False)
    op.drop_column("gathers", "description")


def downgrade() -> None:
    """Downgrade for 7913f5e9f28c."""
    # Add the 'description' column back
    op.add_column(
        "gathers", sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True)
    )

    # Copy data from 'name' to 'description'
    op.execute("UPDATE gathers SET description = name")

    # Make the 'description' column non-nullable
    op.alter_column("gathers", "description", nullable=False)
    op.drop_column("gathers", "name")
