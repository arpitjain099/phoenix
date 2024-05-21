"""Pydantic schemas for the Apify scrapers.

This modules contains a Pydantic schema for each Apify scraper, which:
    - Defines the data structure that we want to use in our system for that scraper.
    - Converts that data structure to the correct structure for the Apify API.
"""
import enum
from typing import Annotated, Dict, List

import pydantic

http_url_adapter = pydantic.TypeAdapter(pydantic.HttpUrl)

UrlStr = Annotated[
    str, pydantic.BeforeValidator(lambda value: str(http_url_adapter.validate_python(value)))
]


class ApifyFacebookPostsInput(pydantic.BaseModel):
    """Input schema for the Apify Facebook posts scraper.

    Ref to relevant Apify actor docs: https://apify.com/apify/facebook-posts-scraper/input-schema
    """

    only_posts_older_than: str = pydantic.Field(
        None,
        serialization_alias="onlyPostsOlderThan",
        description="Fetch posts only older than this date (YYYY-MM-DD)",
    )
    only_posts_newer_than: str = pydantic.Field(
        None,
        serialization_alias="onlyPostsNewerThan",
        description="Fetch posts only newer than this date (YYYY-MM-DD)",
    )
    results_per_url_limit: int = pydantic.Field(
        25, serialization_alias="resultsLimit", description="Limit results per account"
    )
    account_urls: List[UrlStr] = pydantic.Field(
        serialization_alias="startUrls",
        description="List of Facebook page/profile URLs to scrape from",
    )

    class Config:
        """Pydantic configuration."""

        extra = pydantic.Extra.forbid

    @pydantic.field_serializer("account_urls")
    def serialize_account_urls(self, urls: List[pydantic.HttpUrl]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]


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
        False,
        serialization_alias="includeNestedComments",
        description=(
            "If True, includes up to 3 levels of nested comments/replies. "
            "WARNING: this breaks results_limit and will likely return more comments "
            "and incur more cost than expected."
        ),
    )
    comment_sort_option: FacebookCommentSortOption = pydantic.Field(
        FacebookCommentSortOption.RANKED_UNFILTERED,
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
