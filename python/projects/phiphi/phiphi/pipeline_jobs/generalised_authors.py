"""Generalised authors.

Functionality and schemas for generalised authors.
"""
import pandas as pd
import pandera as pa

from phiphi.pipeline_jobs import constants
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


def get_post_authors(
    project_namespace: str,
    offset: int = 0,
    limit: int = 1000,
    deduplicated_authors_table_name: str = (constants.DEDUPLICATED_GENERALISED_AUTHORS_TABLE_NAME),
) -> pd.DataFrame:
    """Retrieve authors with posts, ordered by post_count.

    Args:
        project_namespace (str): The project namespace.
        offset (int, optional): Offset for pagination. Defaults to 0.
        limit (int, optional): Limit for pagination. Defaults to 1000.
        deduplicated_authors_table_name (str, optional): Name of the table containing deduplicated
            generalised authors. Defaults to constants.DEDUPLICATED_GENERALISED_AUTHORS_TABLE_NAME.

    Returns:
        pd.DataFrame: DataFrame containing authors with a post count, adhering to
        the `deduplicated_generalised_authors_schema` schema.

    Raises:
        pa.errors.SchemaError: If schema validation fails for the resulting DataFrame.
    """
    query = f"""
    SELECT *
    FROM `{project_namespace}.{deduplicated_authors_table_name}`
    WHERE post_count > 0
    ORDER BY post_count DESC
    LIMIT {limit}
    OFFSET {offset}
    """
    post_authors_df = pd.read_gbq(query)
    deduplicated_generalised_authors_schema.validate(post_authors_df)
    return post_authors_df
