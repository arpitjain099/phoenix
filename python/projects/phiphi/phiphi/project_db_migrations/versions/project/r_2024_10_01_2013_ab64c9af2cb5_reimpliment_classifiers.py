"""Reimplement classifiers.

Revision ID: ab64c9af2cb5
Revises: 0da2461a263f
Create Date: 2024-10-01 20:13:40.709435

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "ab64c9af2cb5"
down_revision: Union[str, None] = "0da2461a263f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade for ab64c9af2cb5."""
    op.add_column(
        "classified_messages", sa.Column("classifier_version_id", sa.Integer(), nullable=False)
    )
    op.add_column("classified_messages", sa.Column("class_name", sa.String(), nullable=False))
    op.drop_column("classified_messages", "class_id")


def downgrade() -> None:
    """Downgrade for ab64c9af2cb5."""
    op.add_column("classified_messages", sa.Column("class_id", sa.INTEGER(), nullable=False))
    op.drop_column("classified_messages", "class_name")
    op.drop_column("classified_messages", "classifier_version_id")
