"""Intermediatory classified post authors.

Revision ID: 148ded373a7d
Revises: 2471145c028e
Create Date: 2024-10-22 15:18:14.215184

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "148ded373a7d"
down_revision: Union[str, None] = "2471145c028e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade for 148ded373a7d."""
    op.create_table(
        "intermediatory_classified_post_authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("classifier_id", sa.Integer(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("phoenix_platform_message_author_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["class_id"],
            ["intermediatory_classes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["classifier_id"],
            ["classifiers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "classifier_id",
            "class_id",
            "phoenix_platform_message_author_id",
            name="uq_intermediatory_classified_authors",
        ),
    )
    op.create_index(
        "ix_intermediatory_classified_authors",
        "intermediatory_classified_post_authors",
        ["classifier_id", "class_id"],
        unique=False,
    )
    op.create_index(
        "ix_intermediatory_classified_authors_class",
        "intermediatory_classified_post_authors",
        ["class_id"],
        unique=False,
    )
    op.create_index(
        "ix_intermediatory_classified_authors_phoenix_id",
        "intermediatory_classified_post_authors",
        ["phoenix_platform_message_author_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade for 148ded373a7d."""
    op.drop_index(
        "ix_intermediatory_classified_authors_class",
        table_name="intermediatory_classified_post_authors",
    )
    op.drop_index(
        "ix_intermediatory_classified_authors", table_name="intermediatory_classified_post_authors"
    )
    op.drop_table("intermediatory_classified_post_authors")
