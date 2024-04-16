"""instance_runs_model.

Revision ID: 330caa4a9ac4
Revises: df23bee88382
Create Date: 2024-04-15 13:50:57.359770

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "330caa4a9ac4"
down_revision: Union[str, None] = "df23bee88382"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "instance_runs"
INSTANCES_TABLE_NAME = "instances"


def upgrade() -> None:
    """Upgrade for 330caa4a9ac4."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("instance_id", sa.Integer(), nullable=False),
        sa.Column("started_processing_at", sa.DateTime(), nullable=True),
        sa.Column("environment_slug", sa.String(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("failed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(INSTANCES_TABLE_NAME, sa.Column("run_status", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade for 330caa4a9ac4."""
    op.drop_column(INSTANCES_TABLE_NAME, "run_status")
    op.drop_table(TABLE_NAME)
