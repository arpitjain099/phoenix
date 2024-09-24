"""Classified authors table and schema definition.

!!Important!!
The `manually_classified_authors_table` and `manually_classified_authors_schema` should match.
"""
import pandera as pa
import sqlalchemy as sa

from phiphi import project_db
from phiphi.pipeline_jobs import constants
from phiphi.pipeline_jobs import utils as pipeline_jobs_utils

manually_classified_authors_schema = pa.DataFrameSchema(
    {
        "class_name": pa.Column(pa.String, nullable=False),
        "phoenix_platform_author_id": pa.Column(pa.String, nullable=False),
        "last_updated_at": pipeline_jobs_utils.utc_datetime_column(nullable=False),
    }
)


manually_classified_authors_table = sa.Table(
    constants.MANUALLY_CLASSIFIED_AUTHORS_TABLE_NAME,
    project_db.metadata,
    sa.Column("class_name", sa.String, nullable=False),
    sa.Column("phoenix_platform_author_id", sa.String, nullable=False),
    sa.Column("last_updated_at", sa.TIMESTAMP, nullable=False),
)
