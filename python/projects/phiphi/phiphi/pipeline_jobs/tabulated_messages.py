"""Tabulated messages table definition.

It is important that only table definitions are used for bigquery tables. This is due to bigquery
not supporting auto incrementing and applying constraints using a different DDL syntax. This is why
having a different syntax sqlalchemy-bigquery not supporting primary keys, indexes, and other table
constraints.

"""
import sqlalchemy as sa

from phiphi import project_db

tabulated_messages_table = sa.Table(
    "tabulated_messages",
    project_db.metadata,
    # General
    sa.Column("platform", sa.String, nullable=False),
    # Post Author
    sa.Column("post_author_category", sa.String, nullable=True),
    sa.Column("post_author_class", sa.String, nullable=True),
    sa.Column("post_author_description", sa.Text, nullable=True),
    sa.Column("post_author_followers", sa.Integer, nullable=True),
    sa.Column("post_author_id", sa.Integer, nullable=False),
    sa.Column("post_author_location", sa.String, nullable=True),
    sa.Column("post_author_name_pi", sa.String, nullable=True),
    sa.Column("post_author_link_pi", sa.String, nullable=True),
    # Post
    sa.Column("post_class", sa.String, nullable=True),
    sa.Column("post_comment_count", sa.Integer, nullable=True),
    sa.Column("post_date", sa.String, nullable=False),
    sa.Column("post_gather_id", sa.Integer, nullable=False),
    sa.Column("post_id", sa.String, nullable=False),
    sa.Column("post_like_count", sa.Integer, nullable=True),
    sa.Column("post_link_pi", sa.String, nullable=True),
    sa.Column("post_share_count", sa.Integer, nullable=True),
    sa.Column("post_text_pi", sa.Text, nullable=True),
    # Comments author
    sa.Column("comment_author_class", sa.String, nullable=True),
    sa.Column("comment_author_id", sa.String, nullable=False),
    sa.Column("comment_author_name_pi", sa.String, nullable=True),
    # Comments
    sa.Column("comment_class", sa.String, nullable=True),
    sa.Column("comment_date", sa.String, nullable=False),
    sa.Column("comment_gather_id", sa.Integer, nullable=False),
    sa.Column("comment_id", sa.String, nullable=False),
    sa.Column("comment_like_count", sa.Integer, nullable=True),
    sa.Column("comment_link_pi", sa.String, nullable=True),
    sa.Column("comment_parent_post_id", sa.String, nullable=False),
    sa.Column("comment_replied_to_id", sa.String, nullable=True),
    sa.Column("comment_text_pi", sa.Text, nullable=True),
    # Platform specific
    sa.Column("facebook_video_views", sa.Integer, nullable=True),
    sa.Column("tiktok_post_plays", sa.Integer, nullable=True),
)
