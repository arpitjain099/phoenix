"""Schemas for apify facebook post gathers."""

from typing import List, Optional

import pydantic

from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.pydantic_types import UrlStr


class ApifyFacebookPostGatherBase(gather_schemas.GatherBase):
    """Input schema for the Apify Facebook posts scraper.

    Ref to relevant Apify actor docs: https://apify.com/apify/facebook-posts-scraper/input-schema
    """

    limit_posts_per_account: int = pydantic.Field(
        25, serialization_alias="resultsLimit", description="Limit results per account"
    )
    account_url_list: List[UrlStr] = pydantic.Field(
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


class ApifyFacebookPostGatherResponse(gather_schemas.GatherResponse, ApifyFacebookPostGatherBase):
    """Apify Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)


class ApifyFacebookPostGatherCreate(gather_schemas.GatherCreate, ApifyFacebookPostGatherBase):
    """Apify Gather create schema.

    Properties to receive via API on creation.
    """


class ApifyFacebookPostGatherUpdate(gather_schemas.GatherUpdate):
    """Apify Gather update schema."""
