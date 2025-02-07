"""Generalised authors.

Functionality and schemas for generalised authors.
"""
import json

import numpy as np
import pandas as pd
import pandera as pa
from google.api_core import exceptions
from google.cloud import bigquery

from phiphi import config, utils
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

    If `config.settings.USE_MOCK_BQ` is enabled, a sample of generalised authors is returned.
    This is then used for development and testing purposes.

    Be aware that if the table does not exist, the function will raise an error.

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
    if config.settings.USE_MOCK_BQ:
        return load_sample_authors(offset=offset, limit=limit)

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


def get_author(
    project_namespace: str,
    phoenix_platform_message_author_id: str,
    deduplicated_authors_table_name: str = constants.DEDUPLICATED_GENERALISED_AUTHORS_TABLE_NAME,
) -> pd.Series | None:
    """Retrieve a single author with posts.

    If `config.settings.USE_MOCK_BQ` is enabled, an author from the sample of generalised authors
    is returned.
    This is then used for development and testing purposes.

    Be aware that if the table does not exist, the function will raise an error.

    Args:
        project_namespace (str): The project namespace.
        phoenix_platform_message_author_id (str): The phoenix platform message author ID.
        deduplicated_authors_table_name (str, optional): Name of the table containing deduplicated
            generalised authors. Defaults to constants.DEDUPLICATED_GENERALISED_AUTHORS_TABLE_NAME.

    Returns:
        None: If the author is not found.
        pd.Series: Series or a single row containing an author with a post count, adhering to
        the `deduplicated_generalised_authors_schema` schema.

    Raises:
        pa.errors.SchemaError: If schema validation fails for the resulting DataFrame.
    """
    if config.settings.USE_MOCK_BQ:
        all_authors_df = load_sample_authors()
        single_author_df = all_authors_df[
            all_authors_df["phoenix_platform_message_author_id"]
            == phoenix_platform_message_author_id
        ]
        if single_author_df.empty:
            return None
        deduplicated_generalised_authors_schema.validate(single_author_df)
        return single_author_df.iloc[0]

    query = f"""
    SELECT *
    FROM `{project_namespace}.{deduplicated_authors_table_name}`
    WHERE phoenix_platform_message_author_id = '{phoenix_platform_message_author_id}'
    """
    post_author_df = pd.read_gbq(query)
    if post_author_df.empty:
        return None
    deduplicated_generalised_authors_schema.validate(post_author_df)
    return post_author_df.iloc[0]


def load_sample_authors(
    offset: int = 0,
    limit: int = 1000,
) -> pd.DataFrame:
    """Load a sample of generalised authors."""
    path = utils.get_pipeline_sample_data_path("generalised_post_authors.json")
    with open(path, "r") as f:
        sample_authors = json.load(f)

    sample_authors_df = pd.DataFrame(sample_authors)
    deduplicated_generalised_authors_schema.validate(sample_authors_df)
    return sample_authors_df[offset : offset + limit]


def get_total_count_post_authors(
    project_namespace: str,
    deduplicated_authors_table_name: str = constants.DEDUPLICATED_GENERALISED_AUTHORS_TABLE_NAME,
) -> int:
    """Retrieve the total count of authors with posts.

    If the tables do not exist, the function will return 0.

    Args:
        project_namespace (str): The project namespace.
        deduplicated_authors_table_name (str, optional): Name of the table containing deduplicated
            generalised authors. Defaults to constants.DEDUPLICATED_GENERALISED_AUTHORS_TABLE_NAME.

    Returns:
        int: Total count of authors with posts.
    """
    if config.settings.USE_MOCK_BQ:
        return len(load_sample_authors())

    # Initialize BigQuery client
    client = bigquery.Client()

    # Check if the table exists
    table_id = f"{project_namespace}.{deduplicated_authors_table_name}"
    try:
        client.get_table(table_id)  # API request to check table existence
    except exceptions.NotFound:
        return 0

    query = f"""
    SELECT COUNT(*) as count
    FROM `{table_id}`
    WHERE post_count > 0
    """
    # Read data using the utility function
    count_df = pipeline_jobs_utils.read_data(
        query, project_namespace, deduplicated_authors_table_name
    )
    count = count_df.iloc[0]["count"]
    # Needed for mypy
    assert isinstance(count, np.int64)
    return int(count)
