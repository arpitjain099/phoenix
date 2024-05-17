"""Schemas for apify facebook post gathers."""

from typing import Annotated

import pydantic

from phiphi.api.projects.gathers import schemas as gather_schemas


class ApifyFacebookPostGatherBase(gather_schemas.GatherBase):
    """Gather config schema."""

    account_url_list: Annotated[
        list[str],
        pydantic.Field(description="The author url list, should be the full url including https"),
    ]

    limit_posts_per_account: Annotated[
        int,
        pydantic.Field(
            default=1000,
            description="",
        ),
    ]
    only_posts_older_than: Annotated[
        str,
        pydantic.Field(
            description="YYYY-MM-DD format",
        ),
    ]
    only_posts_newer_than: Annotated[
        str,
        pydantic.Field(
            description="YYYY-MM-DD format",
        ),
    ]


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
