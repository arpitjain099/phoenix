"""Functions which take an Apify json blob and normalise it into a standard format."""
import hashlib
import uuid
from datetime import datetime
from typing import Callable, Dict, List, Union

import pandas as pd

from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.pipeline_jobs.gathers import project_db_schemas


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
    project_id: int,
    gather_id: int,
    gather_batch_id: int,
    gathered_at: datetime,
    source: gather_schemas.Source,
    platform: gather_schemas.Platform,
    data_type: gather_schemas.DataType,
) -> pd.DataFrame:
    """Process a list of JSON blobs and normalize them into a DataFrame."""
    normalized_records = [normaliser(blob) for blob in batch_json]
    messages_df = pd.DataFrame(normalized_records)

    # Add constant columns to the DataFrame
    messages_df["project_id"] = project_id
    messages_df["gather_id"] = gather_id
    messages_df["gather_batch_id"] = gather_batch_id
    messages_df["gathered_at"] = gathered_at
    messages_df["source"] = source
    messages_df["platform"] = platform
    messages_df["data_type"] = data_type
    messages_df["phoenix_processed_at"] = datetime.now()

    # Validate the DataFrame using the schema
    project_db_schemas.generalised_messages_schema.validate(messages_df)

    return messages_df
