"""Normalise functionality for the gather pipeline job."""
import json
from datetime import datetime
from typing import Callable, Dict, List

import pandas as pd
import prefect

from phiphi.api.projects import gathers
from phiphi.pipeline_jobs import constants, project_db_schemas, utils
from phiphi.pipeline_jobs.gathers import normalisers

NormaliserFuncType = Callable[[Dict], Dict | None]


def normalise_batch(
    normaliser: NormaliserFuncType,
    batch_json: List[Dict],
    gather: gathers.schemas.GatherResponse,
    gather_batch_id: int,
    gathered_at: datetime,
) -> pd.DataFrame:
    """Process a list of JSON blobs and normalize them into a DataFrame."""
    normalized_records = [
        result for blob in batch_json if (result := normaliser(blob)) is not None
    ]
    messages_df = pd.DataFrame(normalized_records)

    gather_creation_defaults = gathers.child_types.get_gather_project_db_defaults(
        gather.child_type
    )

    # Add constant columns to the DataFrame
    messages_df["gather_id"] = gather.id
    messages_df["gather_batch_id"] = gather_batch_id
    messages_df["gathered_at"] = gathered_at
    messages_df["gather_type"] = gather.child_type
    messages_df["platform"] = gather_creation_defaults.platform
    messages_df["data_type"] = gather_creation_defaults.data_type
    messages_df["phoenix_processed_at"] = datetime.utcnow()

    # Validate the DataFrame using the schema
    validated_df = project_db_schemas.generalised_messages_schema.validate(messages_df)

    return validated_df


gather_normalisation_map: Dict[type[gathers.schemas.GatherResponse], NormaliserFuncType] = {
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse: (
        normalisers.normalise_single_facebook_posts_json
    ),
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentsGatherResponse: (
        normalisers.normalise_single_facebook_comments_json
    ),
    gathers.apify_tiktok_accounts_posts.schemas.ApifyTikTokAccountsPostsGatherResponse: (
        normalisers.normalise_single_tiktok_posts_json
    ),
    gathers.apify_tiktok_hashtags_posts.schemas.ApifyTikTokHashtagsPostsGatherResponse: (
        normalisers.normalise_single_tiktok_posts_json
    ),
    gathers.apify_tiktok_comments.schemas.ApifyTikTokCommentsGatherResponse: (
        normalisers.normalise_single_tiktok_comments_json
    ),
    # Add other gather types and their corresponding normalization functions here
}


@prefect.task
def normalise_batches(
    gather: gathers.schemas.GatherResponse,
    job_run_id: int,
    bigquery_dataset: str,
) -> None:
    """Normalize batches and write to a BigQuery table."""
    prefect_logger = prefect.get_run_logger()
    norm_func = gather_normalisation_map[type(gather)]

    batch_id = 0
    while True:
        query = f"""
            SELECT * FROM {bigquery_dataset}.{constants.GATHER_BATCHES_TABLE_NAME}
            WHERE gather_id = {gather.id} AND job_run_id = {job_run_id} AND batch_id = {batch_id}
        """
        batches_df = utils.read_data(
            query, dataset=bigquery_dataset, table=constants.GATHER_BATCHES_TABLE_NAME
        )

        if batches_df.empty:
            break

        validated_batches_df = project_db_schemas.gather_batches_schema.validate(batches_df)

        for _, batch in validated_batches_df.iterrows():
            prefect_logger.info(f"Normalizing batch {batch.batch_id}")

            batch_json = json.loads(batch.json_data)
            normalized_df = normalise_batch(
                normaliser=norm_func,
                batch_json=batch_json,
                gather=gather,
                gather_batch_id=batch.batch_id,
                gathered_at=batch.gathered_at,
            )

            utils.write_data(
                df=normalized_df,
                dataset=bigquery_dataset,
                table=constants.GENERALISED_MESSAGES_TABLE_NAME,
            )
            prefect_logger.info(f"Batch {batch.batch_id} normalized and written.")

        batch_id += 1
