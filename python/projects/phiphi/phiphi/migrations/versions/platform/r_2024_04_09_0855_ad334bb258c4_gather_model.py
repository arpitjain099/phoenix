"""Gather model.

Revision ID: ad334bb258c4
Revises: f766ea48c9d1
Create Date: 2024-04-09 08:55:29.163130

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ad334bb258c4"
down_revision: Union[str, None] = "f766ea48c9d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "gathers"
APIFY_TABLE_NAME = "apify_gathers"


def upgrade() -> None:
    """Upgrade for ad334bb258c4."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("mark_to_delete", sa.Boolean(), nullable=True),
        sa.Column("last_run_at", sa.DateTime(), nullable=True),
        sa.Column("instance_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("platform", sa.String(), nullable=True),
        sa.Column("data_type", sa.String(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        APIFY_TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("limit_messages", sa.Integer(), nullable=False),
        sa.Column("limit_replies", sa.Integer(), nullable=False),
        sa.Column("nested_replies", sa.Boolean(), nullable=False),
        sa.Column("input_data", sa.String(), nullable=False),
        sa.Column("input_type", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["gathers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade for ad334bb258c4."""
    op.drop_table(APIFY_TABLE_NAME)
    op.drop_table(TABLE_NAME)
