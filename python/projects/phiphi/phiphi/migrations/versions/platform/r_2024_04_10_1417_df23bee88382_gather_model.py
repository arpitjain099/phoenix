"""gather_model.

Revision ID: df23bee88382
Revises: 7cb955da8fb9
Create Date: 2024-04-10 14:17:06.824744

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from phiphi.api import base_models

# revision identifiers, used by Alembic.
revision: str = "df23bee88382"
down_revision: Union[str, None] = "7cb955da8fb9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "gathers"
APIFY_TABLE_NAME = "apify_gathers"


def upgrade() -> None:
    """Upgrade for df23bee88382."""
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
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
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
        sa.Column("input", base_models.JSONEncodedValue(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["gathers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade for 7cb955da8fb9."""
    op.drop_table(APIFY_TABLE_NAME)
    op.drop_table(TABLE_NAME)
