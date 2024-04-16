"""environment_instance_relationship.

Revision ID: 6d4b2c6a304c
Revises: 7cb955da8fb9
Create Date: 2024-04-12 13:55:26.167391

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6d4b2c6a304c"
down_revision: Union[str, None] = "7cb955da8fb9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "instances"


def upgrade() -> None:
    """Upgrade for 6d4b2c6a304c."""
    op.add_column(
        TABLE_NAME,
        sa.Column("environment_slug", sa.String(), nullable=False, server_default="main"),
    )
    op.create_foreign_key(
        "fk_environment_slug", TABLE_NAME, "environments", ["environment_slug"], ["slug"]
    )
    op.drop_column(TABLE_NAME, "environment_id")


def downgrade() -> None:
    """Downgrade for 6d4b2c6a304c."""
    op.add_column(
        TABLE_NAME, sa.Column("environment_id", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.drop_constraint("fk_environment_slug", TABLE_NAME, type_="foreignkey")
    op.drop_column(TABLE_NAME, "environment_slug")
