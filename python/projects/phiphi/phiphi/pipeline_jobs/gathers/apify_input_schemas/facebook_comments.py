"""Pydantic input schema for the Apify Facebook comments scraper."""
import enum
from typing import Dict, List, Optional

import pydantic

from phiphi.pipeline_jobs.gathers.apify_input_schemas.types import UrlStr


class FacebookCommentSortOption(str, enum.Enum):
    """Enum for the sorting options for Facebook comments."""

    RANKED_THREADED = "RANKED_THREADED"
    RECENT_ACTIVITY = "RECENT_ACTIVITY"
    RANKED_UNFILTERED = "RANKED_UNFILTERED"


class ApifyFacebookCommentsInput(pydantic.BaseModel):
    """Input schema for the Apify Facebook comments scraper.

    Ref to relevant Apify actor docs: https://apify.com/apify/facebook-comments-scraper/input-schema
    """

    post_urls: List[UrlStr] = pydantic.Field(
        ...,
        serialization_alias="startUrls",
        description="List of Facebook post URLs to scrape comments from",
    )
    results_limit: int = pydantic.Field(
        25,
        serialization_alias="resultsLimit",
        description="Limit results per post; defaults to 50 if not set",
    )
    include_nested_comments: bool = pydantic.Field(
        default=False,
        serialization_alias="includeNestedComments",
        description=(
            "If True, includes up to 3 levels of nested comments/replies. "
            "WARNING: this breaks results_limit and will likely return more comments "
            "and incur more cost than expected."
        ),
    )
    comment_sort_option: Optional[FacebookCommentSortOption] = pydantic.Field(
        default=None,
        serialization_alias="viewOption",
        description="Sorting option for comments, default is 'RANKED_UNFILTERED'",
    )

    class Config:
        """Pydantic configuration."""

        extra = pydantic.Extra.forbid

    @pydantic.field_serializer("post_urls")
    def serialize_account_urls(self, urls: List[pydantic.HttpUrl]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]
