"""Utility functions for data processing and uploading."""
import os
import re
import warnings

import pandas as pd
import pandera as pa
from prefect import task
from prefect.deployments import deployments

from phiphi import config
from phiphi.api.projects import job_runs


@task
async def run_flow_deployment_as_subflow(
    deployment_name: str,
    flow_params: dict,
    project_id: int,
    job_type: job_runs.schemas.ForeignJobType,
    job_source_id: int,
    job_run_id: int,
) -> None:
    """Run a Prefect flow as a subflow."""
    await deployments.run_deployment(
        name=deployment_name,
        parameters=flow_params,
        as_subflow=True,
        tags=[
            f"project_id:{project_id}",
            f"job_type:{job_type}",
            f"job_source_id:{job_source_id}",
            f"job_run_id:{job_run_id}",
        ],
    )


def write_data(
    df: pd.DataFrame,
    dataset: str,
    table: str,
) -> None:
    """Upload DataFrame to BigQuery, or attempt to use BQ emulation.

    Warning: Not all BQ queries used in the pipelines are supported in the mock/emulated BQ
    environment. Use with caution.

    Future intention is to implement https://github.com/goccy/bigquery-emulator as a local emulator
    for testing, as well as a platform version that doesn't rely on GCP. Not currently implemented.


    Args:
        df (pd.DataFrame): DataFrame to be uploaded or saved.
        dataset (str): BigQuery dataset name.
        table (str): BigQuery table name.
    """
    if config.settings.USE_MOCK_BQ:
        warnings.warn(
            "Not all BQ queries used in the pipelines are supported in the mock/emulated BQ "
            " environment. Use with caution."
        )
        parquet_file_path = os.path.join(
            config.settings.MOCK_BQ_ROOT_DIR, dataset, table + ".parquet"
        )
        os.makedirs(os.path.dirname(parquet_file_path), exist_ok=True)

        if os.path.exists(parquet_file_path):
            existing_df = pd.read_parquet(parquet_file_path)
            df = pd.concat([existing_df, df])  # noqa: PD901

        df.to_parquet(parquet_file_path, index=False)
    else:
        df.to_gbq(destination_table=f"{dataset}.{table}", if_exists="append")


def read_data(query: str, dataset: str, table: str) -> pd.DataFrame:
    """Read data from BigQuery or a local Parquet file based on configuration.

    Args:
        query (str): The SQL query to run when reading from BigQuery.
        dataset (str): BigQuery dataset name.
        table (str): BigQuery table name.

    Returns:
        pd.DataFrame: The resulting DataFrame from the query.
    """
    if config.settings.USE_MOCK_BQ:
        parquet_file_path = os.path.join(
            config.settings.MOCK_BQ_ROOT_DIR, dataset, table + ".parquet"
        )
        if os.path.exists(parquet_file_path):
            full_table_df = pd.read_parquet(parquet_file_path)
            # Simulate SQL query using pandas query
            pd_query = translate_bq_to_pandas_query(query)
            return full_table_df.query(pd_query)
        else:
            raise FileNotFoundError(f"Parquet file not found at {parquet_file_path}")
    else:
        return pd.read_gbq(query)


def translate_bq_to_pandas_query(bq_query: str) -> str:
    """Translate a simple BigQuery query to a Pandas DataFrame query."""
    # Extract the WHERE clause
    match = re.search(r"WHERE (.+)", bq_query, re.IGNORECASE)
    if not match:
        raise ValueError("Only simple WHERE clauses are supported.")
    where_clause = match.group(1)
    # Replace BigQuery operators with Pandas equivalents
    pandas_query = where_clause.replace(" AND ", " and ").replace(" OR ", " or ")
    # Change "=" to "=="
    pandas_query = re.sub(r"(?<!=)=(?!=)", "==", pandas_query)
    # Remove backticks if present
    pandas_query = pandas_query.replace("`", "")
    return pandas_query


def utc_datetime_column(nullable: bool) -> pa.Column:
    """Return a Pandera column for a UTC datetime which coerces.

    Should be used for columns that are expected to be UTC datetimes, and dfs should be passed
    through validation to ensure columns are coerced.
    """
    return pa.Column(
        pa.engines.pandas_engine.DateTime(  # type: ignore[call-arg]
            unit="ms",
            tz="UTC",
        ),
        coerce=True,
        nullable=nullable,
    )
