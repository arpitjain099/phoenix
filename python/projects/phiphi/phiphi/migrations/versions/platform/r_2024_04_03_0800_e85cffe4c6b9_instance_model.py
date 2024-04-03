"""instance_model.

Revision ID: e85cffe4c6b9
Revises: 371b7af746ab
Create Date: 2024-04-03 08:00:09.449899

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e85cffe4c6b9"
down_revision: Union[str, None] = "371b7af746ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE_NAME = "instances"


def upgrade() -> None:
    """Upgrade for e85cffe4c6b9."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("environment_key", sa.String(), nullable=False),
        sa.Column("pi_deleted_after_days", sa.Integer(), nullable=False),
        sa.Column("delete_after_days", sa.Integer(), nullable=False),
        sa.Column("expected_usage", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade for e85cffe4c6b9."""
    op.drop_table(TABLE_NAME)
