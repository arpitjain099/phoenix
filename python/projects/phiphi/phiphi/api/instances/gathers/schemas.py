"""Schemas for gathers."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic


class ApifyGatherInputType(str, Enum):
    """Gather config input type."""

    author_url_list = "author_url_list"


class InputAuthorList(pydantic.BaseModel):
    """Input type and data type of gather."""

    type: Annotated[
        ApifyGatherInputType, pydantic.Field(description="The data type of the gather")
    ]
    data: Annotated[list[str], pydantic.Field(description="The data type of the gather")]


class Platform(str, Enum):
    """Platform enum."""

    facebook = "facebook"


class DataType(str, Enum):
    """data type enum."""

    messages = "messages"


class GatherBase(pydantic.BaseModel):
    """Gather base schema.

    Shared properties of all gathers.
    """

    description: Annotated[str, pydantic.Field(description="The description of the gather")]
    start_date: Annotated[datetime.datetime, pydantic.Field(description="Gather start date")]
    end_date: Annotated[datetime.datetime, pydantic.Field(description="Gather end date")]
    platform: Annotated[Platform | None, pydantic.Field(description="The platform of the gather")]
    data_type: Annotated[
        DataType | None, pydantic.Field(description="The data type of the gather")
    ]
    # instance_id: Annotated[
    #     int,
    #     pydantic.Field(
    #         description="",
    #     ),
    # ]


class ApifyGatherBase(GatherBase):
    """Gather config schema."""

    input: Annotated[
        InputAuthorList, pydantic.Field(description="The input type of gather config input")
    ]

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
    instance_id: int
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
