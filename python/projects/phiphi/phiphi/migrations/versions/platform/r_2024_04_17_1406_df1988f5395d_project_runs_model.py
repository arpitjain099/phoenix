"""project_runs_model.

Revision ID: df1988f5395d
Revises: 6d4b2c6a304c
Create Date: 2024-04-17 14:06:34.847235

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df1988f5395d"
down_revision: Union[str, None] = "6d4b2c6a304c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "project_runs"


def upgrade() -> None:
    """Upgrade for df1988f5395d."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("started_processing_at", sa.DateTime(), nullable=True),
        sa.Column("environment_slug", sa.String(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("failed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade for df1988f5395d."""
    op.drop_table(TABLE_NAME)
