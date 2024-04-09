"""environment_model.

Revision ID: 5f5d487487ed
Revises: f766ea48c9d1
Create Date: 2024-04-09 12:50:00.829390

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5f5d487487ed"
down_revision: Union[str, None] = "f766ea48c9d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "environments"


def upgrade() -> None:
    """Upgrade for 5f5d487487ed."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("unique_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade for 5f5d487487ed."""
    op.drop_table(TABLE_NAME)
