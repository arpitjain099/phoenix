"""Pydantic input schema for the Apify Facebook posts scraper."""
from typing import Dict, List, Optional

import pydantic

from phiphi.pipeline_jobs.gathers.apify_input_schemas.types import UrlStr


class ApifyFacebookPostsInput(pydantic.BaseModel):
    """Input schema for the Apify Facebook posts scraper.

    Ref to relevant Apify actor docs: https://apify.com/apify/facebook-posts-scraper/input-schema
    """

    results_per_url_limit: int = pydantic.Field(
        25, serialization_alias="resultsLimit", description="Limit results per account"
    )
    account_urls: List[UrlStr] = pydantic.Field(
        serialization_alias="startUrls",
        description="List of Facebook page/profile URLs to scrape from",
    )
    only_posts_older_than: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="onlyPostsOlderThan",
        description="Fetch posts only older than this date (YYYY-MM-DD)",
    )
    only_posts_newer_than: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="onlyPostsNewerThan",
        description="Fetch posts only newer than this date (YYYY-MM-DD)",
    )

    class Config:
        """Pydantic configuration."""

        extra = pydantic.Extra.forbid

    @pydantic.field_serializer("account_urls")
    def serialize_account_urls(self, urls: List[pydantic.HttpUrl]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]
