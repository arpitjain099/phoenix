"""Normalise functionality for the gather pipeline job."""
import json
from datetime import datetime
from typing import Callable, Dict, List, Optional

import pandas as pd
import prefect

from phiphi.api.projects import gathers
from phiphi.pipeline_jobs import constants, gather_batches, project_db_schemas, utils
from phiphi.pipeline_jobs.gathers import normalisers

NormaliserFuncType = Callable[[Dict], Dict | None]


def normalise_batch(
    normaliser: NormaliserFuncType,
    batch_json: List[Dict],
    gather_id: int,
    gather_child_type: gathers.schemas.ChildTypeName,
    gather_batch_id: int,
    gathered_at: datetime,
) -> pd.DataFrame | None:
    """Process a list of JSON blobs and normalize them into a DataFrame."""
    normalized_records = [
        result for blob in batch_json if (result := normaliser(blob)) is not None
    ]

    if not normalized_records:
        return None

    messages_df = pd.DataFrame(normalized_records)

    gather_creation_defaults = gathers.child_types.get_gather_project_db_defaults(
        gather_child_type
    )

    # Add constant columns to the DataFrame
    messages_df["gather_id"] = gather_id
    messages_df["gather_batch_id"] = gather_batch_id
    messages_df["gathered_at"] = gathered_at
    messages_df["gather_type"] = gather_child_type
    messages_df["platform"] = gather_creation_defaults.platform
    messages_df["data_type"] = gather_creation_defaults.data_type
    messages_df["phoenix_processed_at"] = datetime.utcnow()

    # Validate the DataFrame using the schema
    validated_df = project_db_schemas.generalised_messages_schema.validate(messages_df)

    return validated_df


gather_normalisation_map: Dict[gathers.schemas.ChildTypeName, NormaliserFuncType] = {
    gathers.schemas.ChildTypeName.apify_facebook_posts: (
        normalisers.normalise_single_facebook_posts_json
    ),
    gathers.schemas.ChildTypeName.apify_facebook_search_posts: (
        normalisers.normalise_single_facebook_search_posts_json
    ),
    gathers.schemas.ChildTypeName.apify_facebook_comments: (
        normalisers.normalise_single_facebook_comments_json
    ),
    gathers.schemas.ChildTypeName.apify_tiktok_accounts_posts: (
        normalisers.normalise_single_tiktok_posts_json
    ),
    gathers.schemas.ChildTypeName.apify_tiktok_hashtags_posts: (
        normalisers.normalise_single_tiktok_posts_json
    ),
    gathers.schemas.ChildTypeName.apify_tiktok_searches_posts: (
        normalisers.normalise_single_tiktok_posts_json
    ),
    gathers.schemas.ChildTypeName.apify_tiktok_comments: (
        normalisers.normalise_single_tiktok_comments_json
    ),
    # Add other gather types and their corresponding normalization functions here
}


@prefect.task
def normalise_batches(
    gather_job_run_pairs: list[tuple[int, int]],
    bigquery_dataset: str,
    batch_of_batches_size: int = 200,
) -> None:
    """Normalize batches and write to a BigQuery table.

    This function reads multiple batches at once from the gather_batches table for multiple
    gather-job_run pairs, normalizes them, and writes the normalized data to the
    generalised_messages table.

    Args:
        gather_job_run_pairs (list[tuple[int, int]]): List of (gather_id, job_run_id) pairs.
        bigquery_dataset (str): The BigQuery dataset.
        batch_of_batches_size (int, optional): The number of batches to read at once. Defaults to
            200. Note that BQ has a row size limit of 10MB, so 200 gives a max 2GB in memory.
    """
    prefect_logger = prefect.get_run_logger()

    gather_job_run_filter = ", ".join(
        [f"({gather_id}, {job_run_id})" for gather_id, job_run_id in gather_job_run_pairs]
    )

    total_processed = 0
    while True:
        query = f"""
            SELECT * FROM {bigquery_dataset}.{constants.GATHER_BATCHES_TABLE_NAME}
            WHERE (gather_id, job_run_id) IN ({gather_job_run_filter})
            ORDER BY gather_id ASC, job_run_id ASC, batch_id ASC
            LIMIT {batch_of_batches_size} OFFSET {total_processed}
        """
        batches_df = utils.read_data(
            query, dataset=bigquery_dataset, table=constants.GATHER_BATCHES_TABLE_NAME
        )

        if batches_df.empty:
            break

        validated_batches_df = gather_batches.gather_batches_schema.validate(batches_df)

        normalized_data = []

        for _, batch in validated_batches_df.iterrows():
            prefect_logger.info(
                f"Normalizing batch {batch.batch_id} for gather_id "
                f"{batch.gather_id}, job_run_id {batch.job_run_id}"
            )
            child_type_name = gathers.schemas.ChildTypeName(batch.gather_type)
            norm_func = gather_normalisation_map[child_type_name]

            batch_json = json.loads(batch.json_data)
            normalized_df = normalise_batch(
                normaliser=norm_func,
                batch_json=batch_json,
                gather_id=batch.gather_id,
                gather_child_type=child_type_name,
                gather_batch_id=batch.batch_id,
                gathered_at=batch.gathered_at,
            )
            if normalized_df is not None:
                normalized_data.append(normalized_df)

        if normalized_data:
            all_normalized_df = pd.concat(normalized_data, ignore_index=True)
            utils.write_data(
                df=all_normalized_df,
                dataset=bigquery_dataset,
                table=constants.GENERALISED_MESSAGES_TABLE_NAME,
            )

            start_batch = validated_batches_df.iloc[0]
            end_batch = validated_batches_df.iloc[-1]
            prefect_logger.info(
                f"Processed batches from (gather_id: {start_batch.gather_id}, job_run_id: "
                f"{start_batch.job_run_id}, batch_id: {start_batch.batch_id}) "
                f"to (gather_id: {end_batch.gather_id}, job_run_id: {end_batch.job_run_id}, "
                f"batch_id: {end_batch.batch_id})"
            )

        total_processed += batch_of_batches_size


def get_gather_and_job_run_ids(
    bigquery_dataset: str, gather_ids: Optional[list[int]] = None
) -> pd.DataFrame:
    """Get the unique gather ID and job run ID for all gather batches.

    Args:
        bigquery_dataset: The BigQuery dataset.
        gather_ids (Optional): The gather IDs to filter for. If none then all gathers will be
            gotten.

    Returns:
        DataFrame: The gather ID and job run ID for all gather batches.
    """
    where_query = ""
    if gather_ids:
        gather_ids_str = ",".join([str(gather_id) for gather_id in gather_ids])
        where_query += f" WHERE gather_id IN ({gather_ids_str}) "
    query = f"""
        SELECT gather_id, job_run_id FROM {bigquery_dataset}.{constants.GATHER_BATCHES_TABLE_NAME}
        {where_query}
        GROUP BY 1, 2
    """
    return utils.read_data(
        query, dataset=bigquery_dataset, table=constants.GATHER_BATCHES_TABLE_NAME
    )
