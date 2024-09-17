"""Schemas for Apify TikTok searches posts gathers.

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


class ApifyTikTokSearchesPostsGatherBase(gather_schemas.GatherBase):
    """Input schema for the Apify TikTok Scraper for searches."""

    limit_posts_per_search: int = pydantic.Field(
        serialization_alias="resultsPerPage", description="Limit results per search"
    )
    # It is important that the name of the property is different from the alias other wise it will
    # not be returned from serialize_to_apify_input
    search_list: list[str] = pydantic.Field(
        serialization_alias="searchQueries",
        description=("List of searches to scrape TikTok videos for."),
    )
    proxy_country_to_gather_from: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="proxyCountryCode",
        description=(
            "Country to use for the proxy to gather from. "
            "If this is set a RESIDENTIAL group will be used and will increase the price."
        ),
    )


class ApifyTikTokSearchesPostsGatherResponse(
    gather_schemas.GatherResponse, ApifyTikTokSearchesPostsGatherBase
):
    """Apify TikTok searches posts gather schema."""

    def serialize_to_apify_input(self) -> dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        apify_dict = super().serialize_to_apify_input()
        # We are adding searchSection to the dictionary as it is a constant for gathering posts.
        apify_dict["searchSection"] = constants.TIKTOK_POST_SEARCH_SECTION
        return apify_dict
