"""Schemas for apify facebook post gathers."""

from typing import Any, Dict, List, Optional

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
    posts_created_after: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="onlyPostsOlderThan",
        description="Fetch posts created after this date (YYYY-MM-DD)",
    )
    posts_created_before: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="onlyPostsNewerThan",
        description="Fetch posts created before this date (YYYY-MM-DD)",
    )


class ApifyFacebookPostGatherResponse(gather_schemas.GatherResponse, ApifyFacebookPostGatherBase):
    """Apify Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    def serialize_to_apify_input(self) -> Dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        apify_dict = super().serialize_to_apify_input()
        if "startUrls" in apify_dict:
            apify_dict["startUrls"] = self.serialize_account_urls(apify_dict["startUrls"])
        return apify_dict

    @staticmethod
    def serialize_account_urls(urls: List[str]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]


class ApifyFacebookPostGatherCreate(gather_schemas.GatherCreate, ApifyFacebookPostGatherBase):
    """Apify Gather create schema.

    Properties to receive via API on creation.
    """


class ApifyFacebookPostGatherUpdate(gather_schemas.GatherUpdate):
    """Apify Gather update schema."""

    limit_posts_per_account: Optional[int] = pydantic.Field(
        default=None, description="Limit results per account"
    )
    account_url_list: Optional[List[UrlStr]] = pydantic.Field(
        default=None, description="List of Facebook page/profile URLs to scrape from"
    )
    posts_created_after: Optional[str] = pydantic.Field(
        default=None, description="Fetch posts created after this date (YYYY-MM-DD)"
    )
    posts_created_before: Optional[str] = pydantic.Field(
        default=None, description="Fetch posts created before this date (YYYY-MM-DD)"
    )
