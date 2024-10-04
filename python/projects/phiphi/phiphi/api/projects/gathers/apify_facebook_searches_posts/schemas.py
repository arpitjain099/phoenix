"""Apify Facebook searches posts gather schemas.

Documentation on actor:
    https://apify.com/danek/facebook-search-rental/input-schema
"""
from typing import Optional

import pydantic


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
