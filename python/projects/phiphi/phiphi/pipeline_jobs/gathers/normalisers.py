"""Functions which take an Apify json blob and normalise it into a standard format."""
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Union


def anonymize(input_value: Union[str, int]) -> str:
    """Generate a UUID hash from a given input value - for anonymization."""
    return str(uuid.UUID(hashlib.md5(str(input_value).encode()).hexdigest()))


def is_apify_scraping_error(json_blob: Dict) -> bool:
    """When apify's scraping fails, it returns a json blob with an 'error' key.

    This is undocumented, but we've seen that blobs have an "error" key, with differing extra
    keys depending on the scraper.
    """
    if "error" in json_blob:
        return True
    return False


def is_empty_result(json_blob: Dict) -> bool:
    """When apify's scraping returns an empty result, it can return a json blob without an id key.

    This is undocumented, but we've seen that tiktok results return "authorMeta" data without
    any messages if the user hasn't posted in the timeframe of the scrape.
    """
    if "id" not in json_blob:
        return True
    return False


def normalise_single_facebook_posts_json(json_blob: Dict) -> Dict | None:
    """Extract fields from a single Facebook post JSON blob to normalized form."""
    if is_apify_scraping_error(json_blob):
        return None

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
        # stats
        "like_count": json_blob.get("likes", 0),
        "share_count": json_blob.get("shares", 0),
        "comment_count": json_blob.get("comments", 0),
    }


def normalise_single_facebook_search_posts_json(json_blob: Dict) -> Dict | None:
    """Extract fields from a single Facebook search post JSON blob to normalized form."""
    if is_apify_scraping_error(json_blob):
        return None

    if "post_id" not in json_blob and "message" in json_blob:
        # This means there was some error
        return None

    return {
        "pi_platform_message_id": json_blob["post_id"],
        "pi_platform_message_author_id": json_blob["author"]["id"],
        "pi_platform_message_author_name": json_blob["author"]["name"],
        "pi_platform_parent_message_id": None,  # Posts don't have parent messages
        "pi_platform_root_message_id": None,  # Posts don't have root messages
        "pi_text": json_blob["message"],
        "pi_platform_message_url": json_blob["url"],
        "platform_message_last_updated_at": datetime.utcfromtimestamp(json_blob["timestamp"]),
        "phoenix_platform_message_id": anonymize(json_blob["post_id"]),
        "phoenix_platform_message_author_id": anonymize(json_blob["author"]["id"]),
        "phoenix_platform_parent_message_id": None,  # Posts don't have parent messages
        "phoenix_platform_root_message_id": None,  # Posts don't have root messages
        # stats
        "like_count": json_blob["reactions"].get("like", 0),
        "share_count": 0,  # Facebook search posts don't have shares
        "comment_count": json_blob.get("comments_count", 0),
    }


def normalise_single_facebook_comments_json(json_blob: Dict) -> Dict | None:
    """Extract fields from a single Facebook comment JSON blob to normalized form."""
    if is_apify_scraping_error(json_blob):
        return None
    # Sometimes the Apify actor's GraphQL API returns what seems to be an empty node, with
    # only the post url, and `"video_home_www_trending_hashtag":[]` as the only key-value pairs.
    if "id" not in json_blob:
        return None

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
        "pi_text": json_blob.get("text", ""),
        "pi_platform_message_url": json_blob["commentUrl"],
        "platform_message_last_updated_at": datetime.fromisoformat(json_blob["date"]),
        "phoenix_platform_message_id": anonymize(json_blob["id"]),
        "phoenix_platform_message_author_id": anonymize(json_blob["profileId"]),
        "phoenix_platform_parent_message_id": anonymize(parent_message_id),
        "phoenix_platform_root_message_id": anonymize(json_blob["facebookId"]),
        # stats
        "like_count": int(json_blob.get("likesCount", 0)),
        # There are no shares of comments for facebook
        "share_count": 0,
        "comment_count": json_blob.get("commentsCount", 0),
    }


def normalise_single_tiktok_posts_json(json_blob: Dict) -> Dict | None:
    """Extract fields from a single TikTok post JSON blob to normalized form.

    This normaliser can be used for all gathers that use the clockwork/tiktok-scraper with the
    `searchSection` input as `/video`. Ref:
    https://apify.com/clockworks/tiktok-scraper/input-schema
    """
    if is_apify_scraping_error(json_blob):
        return None
    if is_empty_result(json_blob):
        return None

    return {
        "pi_platform_message_id": json_blob["id"],
        "pi_platform_message_author_id": json_blob["authorMeta"]["id"],
        "pi_platform_message_author_name": json_blob["authorMeta"]["name"],
        "pi_platform_parent_message_id": None,
        "pi_platform_root_message_id": None,
        "pi_text": json_blob["text"],
        "pi_platform_message_url": json_blob["webVideoUrl"],
        "platform_message_last_updated_at": datetime.fromisoformat(json_blob["createTimeISO"]),
        "phoenix_platform_message_id": anonymize(json_blob["id"]),
        "phoenix_platform_message_author_id": anonymize(json_blob["authorMeta"]["id"]),
        "phoenix_platform_parent_message_id": None,
        "phoenix_platform_root_message_id": None,
        # stats
        "like_count": json_blob.get("diggCount", 0),
        "share_count": json_blob.get("shareCount", 0),
        "comment_count": json_blob.get("commentCount", 0),
    }


def normalise_single_tiktok_comments_json(json_blob: Dict) -> Dict | None:
    """Extract fields from a single TikTok comment JSON blob to normalized form.

    This normaliser can be used for all gathers that use the apidojo/tiktok-comments-scraper actor.
    https://apify.com/apidojo/tiktok-comments-scraper/input-schema
    """
    # Tiktok comments have a "noResults" key if there are no comments for a post
    if "noResults" in json_blob and json_blob["noResults"] is True:
        return None

    # ParentId is the comment of a reply and is not set if it is a top-level comment
    parent_message_id = json_blob.get("parentId", json_blob["awemeId"])
    return {
        "pi_platform_message_id": json_blob["id"],
        "pi_platform_message_author_id": json_blob["user"]["id"],
        "pi_platform_message_author_name": json_blob["user"]["username"],
        "pi_platform_parent_message_id": parent_message_id,
        "pi_platform_root_message_id": json_blob["awemeId"],
        "pi_text": json_blob["text"],
        # Tiktok has no url for comments
        "pi_platform_message_url": None,
        "platform_message_last_updated_at": datetime.fromisoformat(json_blob["createdAt"]),
        "phoenix_platform_message_id": anonymize(json_blob["id"]),
        "phoenix_platform_message_author_id": anonymize(json_blob["user"]["id"]),
        "phoenix_platform_parent_message_id": anonymize(parent_message_id),
        "phoenix_platform_root_message_id": anonymize(json_blob["awemeId"]),
        "like_count": json_blob.get("likeCount", 0),
        # No shares for TikTok comments
        "share_count": 0,
        "comment_count": json_blob.get("replyCount", 0),
    }
