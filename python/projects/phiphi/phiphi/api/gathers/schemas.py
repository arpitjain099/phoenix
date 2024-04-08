"""Schemas for gathers."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic


class GatherType(str, Enum):
    """Gather type enum."""

    apify_facebook_messages = "apify_facebook_messages"


class ApifyGatherInputType(str, Enum):
    """Gather config input type."""

    author_url_list = "author_url_list"


class GatherBase(pydantic.BaseModel):
    """Gather base schema.

    Shared properties of all gathers.
    """

    description: Annotated[str, pydantic.Field(description="The description of the gather")]
    config_type: Annotated[GatherType, pydantic.Field(description="The gather type")]
    instance_id: Annotated[
        int,
        pydantic.Field(
            description="",
        ),
    ]


class ApifyGatherBase(GatherBase):
    """Gather config schema."""

    input_type: Annotated[
        ApifyGatherInputType, pydantic.Field(description="The input type of gather config input")
    ]
    input_data: Annotated[str, pydantic.Field(description="This is dependent on the input type")]
    start_date: Annotated[datetime.datetime, pydantic.Field(description="Gather start date")]
    end_date: Annotated[datetime.datetime, pydantic.Field(description="Gather end date")]
    limit_messages: Annotated[
        int,
        pydantic.Field(
            default=1000,
            description="",
        ),
    ]
    limit_replies: Annotated[
        int,
        pydantic.Field(
            default=100,
            description="",
        ),
    ]
    nested_replies: Annotated[bool, pydantic.Field(default=False, description="")]


class GatherResponse(GatherBase):
    """Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    mark_to_delete: bool | None = None
    deleted_at: datetime.datetime | None = None
    last_run_at: datetime.datetime | None = None


class ApifyGatherResponse(GatherResponse, ApifyGatherBase):
    """Apify Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)


class GatherCreate(GatherBase):
    """Gather create schema.

    Properties to receive via API on creation.
    """


class ApifyGatherCreate(ApifyGatherBase):
    """Apify Gather create schema.

    Properties to receive via API on creation.
    """


class GatherUpdate(pydantic.BaseModel):
    """Gather update schema."""

    mark_to_delete: bool


class ApifyGatherUpdate(GatherUpdate):
    """Apify Gather update schema."""
