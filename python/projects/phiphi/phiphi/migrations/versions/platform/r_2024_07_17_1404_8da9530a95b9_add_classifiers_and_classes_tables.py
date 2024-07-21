"""Add_classifiers_and_classes_tables.

Revision ID: 8da9530a95b9
Revises: 16684153ddc6
Create Date: 2024-07-17 14:04:57.953669

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from phiphi.api import base_models

revision: str = "8da9530a95b9"
down_revision: Union[str, None] = "16684153ddc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade for 8da9530a95b9."""
    op.create_table(
        "classes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("class_name", sa.String(), nullable=False),
        sa.Column("class_description", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "classifiers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("classifier_name", sa.String(), nullable=False),
        sa.Column("classifier_type", sa.String(), nullable=False),
        sa.Column("classifier_params", base_models.JSONEncodedValue(), nullable=True),
        sa.Column("archived_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade for 8da9530a95b9."""
    op.drop_table("classifiers")
    op.drop_table("classes")
