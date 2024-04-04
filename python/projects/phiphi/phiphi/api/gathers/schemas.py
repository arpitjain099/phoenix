"""Schemas for gathers."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic


class GatherType(str, Enum):
    """Gather type enum."""

    apify_facebook_messages = "apify_facebook_messages"


class GatherConfigInputType(str, Enum):
    """Gather config input type."""

    author_url_list = "author_url_list"


class GatherConfig(pydantic.BaseModel):
    """Gather config schema."""

    config_input: Annotated[GatherConfigInputType, pydantic.Field(description="")]
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


class GatherBase(pydantic.BaseModel):
    """Gather base schema.

    Shared properties of all gathers.
    """

    description: Annotated[str, pydantic.Field(description="The description of the gather")]
    config_type: Annotated[GatherType, pydantic.Field(description="The gather type")]
    config: Annotated[GatherConfig, pydantic.Field(description="Gather configurations")]


class GatherConfigInput(pydantic.BaseModel):
    """Gather config input."""

    input_type: Annotated[
        GatherConfigInputType, pydantic.Field(description="The input type of gather config input")
    ]
    data: Annotated[str, pydantic.Field(description="This is dependent on the input type")]


class Gather(GatherBase):
    """Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)


class GatherCreate(GatherBase):
    """Gather create schema.

    Properties to receive via API on creation.
    """


class GatherUpdate(pydantic.BaseModel):
    """Gather update schema."""
