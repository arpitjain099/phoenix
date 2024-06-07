"""Functions which take an Apify json blob and normalise it into a standard format."""
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Union


def anonymize(input_value: Union[str, int]) -> str:
    """Generate a UUID hash from a given input value - for anonymization."""
    return str(uuid.UUID(hashlib.md5(str(input_value).encode()).hexdigest()))


def normalise_single_facebook_posts_json(json_blob: Dict) -> Dict:
    """Extract fields from a single Facebook post JSON blob to normalized form."""
    return {
        "pi_platform_message_id": json_blob["postId"],
        "pi_platform_message_author_id": json_blob["user"]["id"],
        "pi_platform_message_author_name": json_blob["user"]["name"],
        "pi_platform_parent_message_id": None,  # Posts don't have parent messages
        "pi_platform_root_message_id": None,  # Posts don't have root messages
        "pi_text": json_blob["text"],
        "pi_platform_message_url": json_blob["url"],
        "platform_message_last_updated_at": datetime.fromisoformat(json_blob["time"]),
        "phoenix_platform_message_id": anonymize(json_blob["postId"]),
        "phoenix_platform_message_author_id": anonymize(json_blob["user"]["id"]),
        "phoenix_platform_parent_message_id": None,  # Posts don't have parent messages
        "phoenix_platform_root_message_id": None,  # Posts don't have root messages
    }


def normalise_single_facebook_comments_json(json_blob: Dict) -> Dict:
    """Extract fields from a single Facebook comment JSON blob to normalized form."""
    if "replyToCommentId" in json_blob:
        parent_message_id = json_blob["replyToCommentId"]
    else:
        parent_message_id = json_blob["facebookId"]

    return {
        "pi_platform_message_id": json_blob["id"],
        "pi_platform_message_author_id": json_blob["profileId"],
        "pi_platform_message_author_name": json_blob["profileName"],
        "pi_platform_parent_message_id": parent_message_id,
        "pi_platform_root_message_id": json_blob["facebookId"],
        "pi_text": json_blob["text"],
        "pi_platform_message_url": json_blob["commentUrl"],
        "platform_message_last_updated_at": datetime.fromisoformat(json_blob["date"]),
        "phoenix_platform_message_id": anonymize(json_blob["id"]),
        "phoenix_platform_message_author_id": anonymize(json_blob["profileId"]),
        "phoenix_platform_parent_message_id": anonymize(parent_message_id),
        "phoenix_platform_root_message_id": anonymize(json_blob["facebookId"]),
    }
