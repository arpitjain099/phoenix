"""Generalised authors.

Functionality and schemas for generalised authors.
"""
import pandera as pa

from phiphi.pipeline_jobs import utils as pipeline_jobs_utils

# Any updates made to this schema should be reflected in `refresh_deduplicated_authors_tables` in
# `pipeline_jobs/gathers/deduplicate.py`
deduplicated_generalised_authors_schema = pa.DataFrameSchema(
    {
        "phoenix_platform_message_author_id": pa.Column(pa.String, nullable=False),
        "pi_platform_message_author_id": pa.Column(pa.String, nullable=False),
        "pi_platform_message_author_name": pa.Column(pa.String, nullable=False),
        "phoenix_processed_at": pipeline_jobs_utils.utc_datetime_column(nullable=False),
        "platform": pa.Column(pa.String, nullable=False),
        "post_count": pa.Column(pa.Int, nullable=False),
        "comment_count": pa.Column(pa.Int, nullable=False),
    }
)
