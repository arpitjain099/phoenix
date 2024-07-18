"""Improve_classifies_classes_column_names.

Revision ID: 5eb071207c24
Revises: 8da9530a95b9
Create Date: 2024-07-18 15:09:24.624749

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from phiphi.api import base_models

revision: str = "5eb071207c24"
down_revision: Union[str, None] = "8da9530a95b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade for 5eb071207c24."""
    op.add_column("classes", sa.Column("name", sa.String(), nullable=False))
    op.add_column("classes", sa.Column("description", sa.String(), nullable=False))
    op.drop_column("classes", "class_name")
    op.drop_column("classes", "class_description")

    op.add_column("classifiers", sa.Column("name", sa.String(), nullable=False))
    op.add_column("classifiers", sa.Column("type", sa.String(), nullable=False))
    op.add_column(
        "classifiers",
        sa.Column("params", base_models.JSONEncodedValue(), nullable=True),
    )
    op.drop_column("classifiers", "classifier_params")
    op.drop_column("classifiers", "classifier_name")
    op.drop_column("classifiers", "classifier_type")


def downgrade() -> None:
    """Downgrade for 5eb071207c24."""
    op.add_column(
        "classifiers",
        sa.Column("classifier_type", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "classifiers",
        sa.Column("classifier_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "classifiers",
        sa.Column("classifier_params", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("classifiers", "params")
    op.drop_column("classifiers", "type")
    op.drop_column("classifiers", "name")

    op.add_column(
        "classes",
        sa.Column("class_description", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "classes", sa.Column("class_name", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.drop_column("classes", "description")
    op.drop_column("classes", "name")
