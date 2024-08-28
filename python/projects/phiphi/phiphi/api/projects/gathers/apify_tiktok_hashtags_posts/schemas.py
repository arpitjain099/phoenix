"""Schemas for Apify TikTok hashtags posts gathers.

This schemas is a subset of the available inputs for the Apify TikTok Scraper.

For reference see the Apify actor docs:
https://apify.com/clockworks/tiktok-scraper/input-schema
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
    posts_created_after: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="oldestPostDate",
        description="Fetch posts created after this date (YYYY-MM-DD)",
    )
    posts_created_since_num_days: Optional[int] = pydantic.Field(
        default=None,
        serialization_alias="scrapeLastNDays",
        description=(
            "Specify how old the scraped videos should be (in days). "
            "Putting 1 will get you only today's posts, 2 - yesterday's and today's, and so on. "
            "If the posts_created_after field was set, "
            "the most recent videos will be scraped. "
            "See docs of field for more information: "
            "https://apify.com/clockworks/tiktok-scraper/input-schema#scrapeLastNDays"
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
    posts_created_after: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="oldestPostDate",
        description="Fetch posts created after this date (YYYY-MM-DD)",
    )
    posts_created_since_num_days: Optional[int] = pydantic.Field(
        default=None,
        serialization_alias="scrapeLastNDays",
        description=(
            "Specify how old the scraped videos should be (in days). "
            "Putting 1 will get you only today's posts, 2 - yesterday's and today's, and so on. "
            "If the posts_created_after field was set, "
            "the most recent videos will be scraped. "
            "See docs of field for more information: "
            "https://apify.com/clockworks/tiktok-scraper/input-schema#scrapeLastNDays"
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
