"""Pydantic schemas for the Apify scrapers.

This modules contains a Pydantic schema for each Apify scraper, which:
    - Defines the data structure that we want to use in our system for that scraper.
    - Converts that data structure to the correct structure for the Apify API.
"""
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
        """Pydantic configuration to allow population by field name."""

        extra = pydantic.Extra.forbid

    @pydantic.field_serializer("account_urls")
    def serialize_account_urls(self, urls: List[pydantic.HttpUrl]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]
