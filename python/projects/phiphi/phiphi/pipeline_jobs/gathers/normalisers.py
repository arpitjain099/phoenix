"""Functions which take an Apify json blob and normalise it into a standard format."""
import hashlib
import json
import uuid
from datetime import datetime
from typing import Callable, Dict, List, Union

import pandas as pd
import prefect

from phiphi.api.projects import gathers
from phiphi.pipeline_jobs import utils
from phiphi.pipeline_jobs.gathers import constants, project_db_schemas


def anonymize(input_value: Union[str, int]) -> str:
    """Generate a UUID hash from a given input value - for anonymization."""
    return str(uuid.UUID(hashlib.md5(str(input_value).encode()).hexdigest()))


def normalise_single_facebook_posts_json(json_blob: Dict) -> Dict:
    """Extract fields from a single Facebook post JSON blob to normalized form."""
    platform_message_last_updated_at = datetime.fromisoformat(json_blob["time"][:-1])
    return {
        "pi_platform_message_id": json_blob["postId"],
        "pi_platform_message_author_id": json_blob["user"]["id"],
        "pi_platform_message_author_name": json_blob["user"]["name"],
        "pi_platform_parent_message_id": None,  # Posts don't have parent messages
        "pi_text": json_blob["text"],
        "pi_platform_message_url": json_blob["url"],
        "platform_message_last_updated_at": platform_message_last_updated_at,
        "phoenix_platform_message_id": anonymize(json_blob["postId"]),
        "phoenix_platform_message_author_id": anonymize(json_blob["user"]["id"]),
        "phoenix_platform_parent_message_id": None,  # Posts don't have parent messages
    }


def normalise_batch(
    normaliser: Callable[[Dict], Dict],
    batch_json: List[Dict],
    gather: gathers.schemas.GatherResponse,
    gather_batch_id: int,
    gathered_at: datetime,
) -> pd.DataFrame:
    """Process a list of JSON blobs and normalize them into a DataFrame."""
    normalized_records = [normaliser(blob) for blob in batch_json]
    messages_df = pd.DataFrame(normalized_records)

    # Add constant columns to the DataFrame
    messages_df["project_id"] = gather.project_id
    messages_df["gather_id"] = gather.id
    messages_df["gather_batch_id"] = gather_batch_id
    messages_df["gathered_at"] = gathered_at
    messages_df["source"] = gather.source
    messages_df["platform"] = gather.platform
    messages_df["data_type"] = gather.data_type
    messages_df["phoenix_processed_at"] = datetime.utcnow()

    # Validate the DataFrame using the schema
    validated_df = project_db_schemas.generalised_messages_schema.validate(messages_df)

    return validated_df


gather_normalisation_map: Dict[type[gathers.schemas.GatherResponse], Callable[[Dict], Dict]] = {
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse: (
        normalise_single_facebook_posts_json
    ),
    # Add other gather types and their corresponding normalization functions here
}


@prefect.task
def normalise_batches(
    gather: gathers.schemas.GatherResponse,
    batch_size: int,
    bigquery_dataset: str,
) -> None:
    """Normalize batches and write to a BigQuery table."""
    prefect_logger = prefect.get_run_logger()
    norm_func = gather_normalisation_map[type(gather)]

    query = f"""
        SELECT * FROM {bigquery_dataset}.{constants.GATHER_BATCHES_TABLE_NAME}
        WHERE gather_id = {gather.id}
    """
    batches_df = utils.read_data(
        query, dataset=bigquery_dataset, table=constants.GATHER_BATCHES_TABLE_NAME
    )
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
