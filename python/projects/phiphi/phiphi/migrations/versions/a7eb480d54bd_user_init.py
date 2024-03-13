"""User init.

Revision ID: a7eb480d54bd
Revises:
Create Date: 2024-03-13 08:45:10.369267

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7eb480d54bd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade for a7eb480d54bd."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)


def downgrade() -> None:
    """Downgrade for a7eb480d54bd."""
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
