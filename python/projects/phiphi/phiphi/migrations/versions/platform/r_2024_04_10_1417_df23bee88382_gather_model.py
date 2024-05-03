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
APIFY_TABLE_NAME = "apify_facebook_post_gathers"


def upgrade() -> None:
    """Upgrade for df23bee88382."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("platform", sa.String(), nullable=True),
        sa.Column("data_type", sa.String(), nullable=True),
        sa.Column("child_type", sa.String(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        APIFY_TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("limit_posts_per_account", sa.Integer(), nullable=False),
        sa.Column("only_posts_older_than", sa.String(), nullable=True),
        sa.Column("only_posts_newer_than", sa.String(), nullable=True),
        sa.Column("author_url_list", base_models.JSONEncodedValue(), nullable=True),
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
