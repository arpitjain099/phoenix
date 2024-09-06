"""Schemas for Apify TikTok hashtags posts gathers.

This schemas is a subset of the available inputs for the Apify TikTok Scraper.

For reference see the Apify actor docs:
https://apify.com/clockworks/tiktok-scraper/input-schema

Note on `posts_created_after` and `posts_created_since_num_days` that these fields don't work for
searches. See issue:
https://apify.com/clockworks/tiktok-scraper/issues/trying-to-set-a-time-RYR6bQdcvzc52hwnO
"""
from typing import Any, Optional

import pydantic

from phiphi.api.projects.gathers import constants
from phiphi.api.projects.gathers import schemas as gather_schemas


class ApifyTikTokHashtagsPostsGatherBase(gather_schemas.GatherBase):
    """Input schema for the Apify TikTok Scraper for hashtags."""

    limit_posts_per_hashtag: int = pydantic.Field(
        serialization_alias="resultsPerPage", description="Limit results per hashtag"
    )
    # It is important that the name of the property is different from the alias other wise it will
    # not be returned from serialize_to_apify_input
    hashtag_list: list[str] = pydantic.Field(
        serialization_alias="hashtags",
        description=(
            "List of hashtags to scrape TikTok videos for. "
            " It is recommended to use without # prefix but "
            "there seems to be no difference when using with."
        ),
    )
    proxy_country_to_gather_from: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="proxyCountryCode",
        description=(
            "Country to use for the proxy to gather from. "
            "If this is set a RESIDENTIAL group will be used and will increase the price."
        ),
    )


class ApifyTikTokHashtagsPostsGatherResponse(
    gather_schemas.GatherResponse, ApifyTikTokHashtagsPostsGatherBase
):
    """Apify TikTok hashtags posts gather schema."""

    def serialize_to_apify_input(self) -> dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        apify_dict = super().serialize_to_apify_input()
        # We are adding searchSection to the dictionary as it is a constant for gathering posts.
        apify_dict["searchSection"] = constants.TIKTOK_POST_SEARCH_SECTION
        return apify_dict


class ApifyTikTokHashtagsPostsGatherCreate(
    gather_schemas.GatherCreate, ApifyTikTokHashtagsPostsGatherBase
):
    """Apify Gather create schema.

    Properties to receive via API on creation.
    """


class ApifyTikTokHashtagsPostsGatherUpdate(gather_schemas.GatherUpdate):
    """Apify Gather update schema."""

    limit_posts_per_hashtag: Optional[int] = pydantic.Field(
        serialization_alias="resultsPerPage", description="Limit results per hashtag"
    )
    # It is important that the name of the property is different from the alias other wise it will
    # not be returned from serialize_to_apify_input
    hashtag_list: Optional[list[str]] = pydantic.Field(
        serialization_alias="hashtags",
        description=(
            "List of hashtags to scrape TikTok videos for. "
            " It is recommended to use without # prefix but "
            "there seems to be no difference when using with."
        ),
    )
    proxy_country_to_gather_from: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="proxyCountryCode",
        description=(
            "Country to use for the proxy to gather from. "
            "If this is set a RESIDENTIAL group will be used and will increase the price."
        ),
    )
