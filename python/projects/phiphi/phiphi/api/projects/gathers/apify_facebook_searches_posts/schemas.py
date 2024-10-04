"""Apify Facebook searches posts gather schemas.

Documentation on actor:
    https://apify.com/danek/facebook-search-rental/input-schema
"""
from typing import Any, Dict, Optional

import pydantic

from phiphi.api.projects.gathers import constants
from phiphi.api.projects.gathers import schemas as gather_schemas


class ApifyProxyConfig(pydantic.BaseModel):
    """Apify Proxy config.

    This schema was inferred by experimenting with the inputs of the actor in the Apify console.
    It is not documented in the actor's documentation.
    """

    use_apify_proxy: bool = pydantic.Field(
        default=False,
        serialization_alias="useApifyProxy",
        description="Whether to use Apify Proxy.",
    )
    apify_proxy_groups: Optional[list[str]] = pydantic.Field(
        default=None,
        serialization_alias="apifyProxyGroups",
        description="List of Apify Proxy groups to use.",
    )
    apify_proxy_country: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="apifyProxyCountry",
        description="Country of Apify Proxy to use.",
    )

    @pydantic.model_validator(mode="after")
    def validate_proxy_settings(self):
        """Validate proxy settings."""
        use_proxy = self.use_apify_proxy
        groups = self.apify_proxy_groups
        country = self.apify_proxy_country

        if not use_proxy:
            if groups is not None:
                raise ValueError(
                    'When "use_apify_proxy" is False, "apify_proxy_country" must not be provided.'
                )
            if country is not None:
                raise ValueError(
                    'When "use_apify_proxy" is False, "apify_proxy_groups" must not be provided.'
                )
        return self


class ApifyFacebookSearchesPostsGatherBase(gather_schemas.GatherBase):
    """Input schema for the Apify Facebook searches posts scraper."""

    search_list: list[str] = pydantic.Field(
        serialization_alias="query",
        description="List of search queries for Facebook posts.",
    )
    limit_posts_per_search: int = pydantic.Field(
        serialization_alias="max_posts", description="Limit results per search query."
    )
    limit_retries_per_search: int = pydantic.Field(
        serialization_alias="max_retries", description="Limit retries per search query."
    )
    recent_posts: Optional[bool] = pydantic.Field(
        default=True,
        serialization_alias="recent_posts",
        description=(
            "Whether to check the recent posts element for posts search, "
            "see https://www.facebook.com/search/posts?q=hello "
            "for the UI input and an example. "
            "Defaults to True."
        ),
    )
    proxy: Optional[ApifyProxyConfig] = pydantic.Field(
        default=None,
        description="Apify proxy to use for the gather.",
    )


class ApifyFacebookSearchesPostsGatherResponse(
    gather_schemas.GatherResponse, ApifyFacebookSearchesPostsGatherBase
):
    """Apify Facebook searches posts gather schema."""

    def serialize_to_apify_input(self) -> Dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        apify_dict = super().serialize_to_apify_input()
        # Add the search type to the apify_dict as this must always be posts.
        apify_dict["search_type"] = constants.FACEBOOK_POST_SEARCH_TYPE
        return apify_dict
