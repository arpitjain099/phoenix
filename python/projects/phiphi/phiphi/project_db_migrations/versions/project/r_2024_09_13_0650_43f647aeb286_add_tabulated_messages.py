"""Add tabulated_messages.

Revision ID: 43f647aeb286
Create Date: 2024-09-13 06:50:14.811014

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "43f647aeb286"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade for 43f647aeb286."""
    op.create_table(
        "tabulated_messages",
        sa.Column("platform", sa.String(), nullable=False),
        sa.Column("post_author_category", sa.String(), nullable=True),
        sa.Column("post_author_class", sa.String(), nullable=True),
        sa.Column("post_author_description", sa.Text(), nullable=True),
        sa.Column("post_author_followers", sa.Integer(), nullable=True),
        sa.Column("post_author_id", sa.Integer(), nullable=False),
        sa.Column("post_author_location", sa.String(), nullable=True),
        sa.Column("post_author_name_pi", sa.String(), nullable=True),
        sa.Column("post_author_link_pi", sa.String(), nullable=True),
        sa.Column("post_class", sa.String(), nullable=True),
        sa.Column("post_comment_count", sa.Integer(), nullable=True),
        sa.Column("post_date", sa.String(), nullable=False),
        sa.Column("post_gather_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.String(), nullable=False),
        sa.Column("post_like_count", sa.Integer(), nullable=True),
        sa.Column("post_link_pi", sa.String(), nullable=True),
        sa.Column("post_share_count", sa.Integer(), nullable=True),
        sa.Column("post_text_pi", sa.Text(), nullable=True),
        sa.Column("comment_author_class", sa.String(), nullable=True),
        sa.Column("comment_author_id", sa.String(), nullable=False),
        sa.Column("comment_author_name_pi", sa.String(), nullable=True),
        sa.Column("comment_class", sa.String(), nullable=True),
        sa.Column("comment_date", sa.String(), nullable=False),
        sa.Column("comment_gather_id", sa.Integer(), nullable=False),
        sa.Column("comment_id", sa.String(), nullable=False),
        sa.Column("comment_like_count", sa.Integer(), nullable=True),
        sa.Column("comment_link_pi", sa.String(), nullable=True),
        sa.Column("comment_parent_post_id", sa.String(), nullable=False),
        sa.Column("comment_replied_to_id", sa.String(), nullable=True),
        sa.Column("comment_text_pi", sa.Text(), nullable=True),
        sa.Column("facebook_video_views", sa.Integer(), nullable=True),
        sa.Column("tiktok_post_plays", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade for 43f647aeb286."""
    op.drop_table("tabulated_messages")
