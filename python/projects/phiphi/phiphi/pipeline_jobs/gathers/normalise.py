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
    gathers.schemas.ChildTypeName.apify_facebook_comments: (
        normalisers.normalise_single_facebook_comments_json
    ),
    gathers.schemas.ChildTypeName.apify_tiktok_accounts_posts: (
        normalisers.normalise_single_tiktok_posts_json
    ),
    gathers.schemas.ChildTypeName.apify_tiktok_hashtags_posts: (
        normalisers.normalise_single_tiktok_posts_json
    ),
    gathers.schemas.ChildTypeName.apify_tiktok_comments: (
        normalisers.normalise_single_tiktok_comments_json
    ),
    # Add other gather types and their corresponding normalization functions here
}


@prefect.task
def normalise_batches(
    gather_id: int,
    job_run_id: int,
    bigquery_dataset: str,
) -> None:
    """Normalize batches and write to a BigQuery table.

    This function reads one batch at a time from the gather_batches table, normalizes it, and
    writes the normalized data to the generalised_messages table.

    It does this one batch at a time to fix the memory footprint of the function and allow for a
    predictable runtime memory usage.

    Args:
        gather_id: The gather ID.
        job_run_id: The job run ID.
        bigquery_dataset: The BigQuery dataset.
    """
    prefect_logger = prefect.get_run_logger()

    batch_id = 0
    # Using a while loop to read one batch at a time
    # This is to keep the memory footprint of the function low/predictable based on batch size of
    # the gathered data.
    while True:
        query = f"""
            SELECT * FROM {bigquery_dataset}.{constants.GATHER_BATCHES_TABLE_NAME}
            WHERE gather_id = {gather_id} AND job_run_id = {job_run_id} AND batch_id = {batch_id}
        """
        batches_df = utils.read_data(
            query, dataset=bigquery_dataset, table=constants.GATHER_BATCHES_TABLE_NAME
        )

        if batches_df.empty:
            break

        validated_batches_df = gather_batches.gather_batches_schema.validate(batches_df)

        for _, batch in validated_batches_df.iterrows():
            prefect_logger.info(f"Normalizing batch {batch.batch_id}")
            child_type_name = gathers.schemas.ChildTypeName(batch.gather_type)
            norm_func = gather_normalisation_map[child_type_name]

            batch_json = json.loads(batch.json_data)
            normalized_df = normalise_batch(
                normaliser=norm_func,
                batch_json=batch_json,
                gather_id=gather_id,
                gather_child_type=child_type_name,
                gather_batch_id=batch.batch_id,
                gathered_at=batch.gathered_at,
            )
            if normalized_df is None:
                continue

            utils.write_data(
                df=normalized_df,
                dataset=bigquery_dataset,
                table=constants.GENERALISED_MESSAGES_TABLE_NAME,
            )
            prefect_logger.info(f"Batch {batch.batch_id} normalized and written.")

        batch_id += 1


def get_gather_and_job_run_ids(
    bigquery_dataset: str, gather_ids: Optional[list[int]] = None
) -> pd.DataFrame:
    """Get the gather ID and job run ID for all gather batches.

    Args:
        bigquery_dataset: The BigQuery dataset.
        gather_ids (Optional): The gather IDs to filter for. If none then all gathers will be
            gotten.

    Returns:
        DataFrame: The gather ID and job run ID for all gather batches.
    """
    query = f"""
        SELECT gather_id, job_run_id FROM {bigquery_dataset}.{constants.GATHER_BATCHES_TABLE_NAME}
    """
    if gather_ids:
        gather_ids_str = ",".join([str(gather_id) for gather_id in gather_ids])
        query += f" WHERE gather_id IN ({gather_ids_str})"
    return utils.read_data(
        query, dataset=bigquery_dataset, table=constants.GATHER_BATCHES_TABLE_NAME
    )
