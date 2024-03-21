"""User Init.

Revision ID: 72a14c8862d1
Revises: fc14296708b6
Create Date: 2024-03-20 16:08:08.432579

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "72a14c8862d1"
down_revision: Union[str, None] = "fc14296708b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "users"
SCHEMA = "platform"


def upgrade() -> None:
    """Upgrade for 72a14c8862d1."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema=SCHEMA,
    )
    op.create_index(
        op.f("ix_platform_users_email"), TABLE_NAME, ["email"], unique=True, schema=SCHEMA
    )


def downgrade() -> None:
    """Downgrade for 72a14c8862d1."""
    op.drop_index(op.f("ix_platform_users_email"), table_name=TABLE_NAME, schema=SCHEMA)
    op.drop_table(TABLE_NAME, schema=SCHEMA)
