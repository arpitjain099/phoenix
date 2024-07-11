"""Schemas for Apify TikTok accounts posts gathers.

This schemas is a subset of the available inputs for the Apify TikTok Scraper.

For reference see the Apify actor docs:
https://apify.com/clockworks/tiktok-scraper/input-schema
"""
from typing import Any, Optional

import pydantic

from phiphi.api.projects.gathers import constants
from phiphi.api.projects.gathers import schemas as gather_schemas


class ApifyTikTokAccountsPostsGatherBase(gather_schemas.GatherBase):
    """Input schema for the Apify TikTok Scraper for accounts."""

    limit_posts_per_account: int = pydantic.Field(
        1, serialization_alias="resultsPerPage", description="Limit results per account"
    )
    account_username_list: list[str] = pydantic.Field(
        serialization_alias="profiles",
        description="List of TikTok account usernames.",
    )
    posts_created_after: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="oldestPostDate",
        description="Fetch posts created after this date (YYYY-MM-DD)",
    )
    posts_created_since_no_days: Optional[int] = pydantic.Field(
        default=None,
        serialization_alias="scrapeLastNDays",
        description=(
            "Specify how old the scraped videos should be (in days)."
            " Putting 1 will get you only today's posts, 2 - yesterday's and today's, and so on."
            " If the Scrape videos newer than field above was set,"
            " the most recent videos will be scraped."
        ),
    )
    proxy_country_to_gather_from: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="proxyCountryCode",
        description=(
            "Country to use for the proxy to gather from."
            " If this is set a RESIDENTIAL group will be used and will increase the price."
        ),
    )


class ApifyTikTokAccountsPostsGatherResponse(
    gather_schemas.GatherResponse, ApifyTikTokAccountsPostsGatherBase
):
    """Apify TikTok hashtags posts gather schema."""

    def serialize_to_apify_input(self) -> dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        apify_dict = super().serialize_to_apify_input()
        # We are adding searchSection to the dictionary as it is a constant for gathering posts.
        apify_dict["searchSection"] = constants.TIKTOK_POST_SEARCH_SECTION
        return apify_dict
