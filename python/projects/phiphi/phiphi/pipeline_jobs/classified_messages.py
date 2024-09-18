"""Classified Messages table definition."""
import sqlalchemy as sa

from phiphi import project_db

classified_messages_table = sa.Table(
    "classified_messages",
    project_db.metadata,
    sa.Column("classifier_id", sa.Integer, nullable=False),
    sa.Column("class_id", sa.Integer, nullable=False),
    sa.Column("phoenix_platform_message_id", sa.String, nullable=False),
    sa.Column("job_run_id", sa.Integer, nullable=False),
)
