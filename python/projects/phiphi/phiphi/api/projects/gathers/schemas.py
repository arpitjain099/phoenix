"""Schemas for gathers."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic


class Platform(str, Enum):
    """Platform enum."""

    facebook = "facebook"


class DataType(str, Enum):
    """data type enum."""

    posts = "posts"


class Source(str, Enum):
    """source enum."""

    apify = "apify"


class GatherBase(pydantic.BaseModel):
    """Gather base schema.

    Shared properties of all gathers.
    """

    description: Annotated[str, pydantic.Field(description="The description of the gather")]
    platform: Annotated[Platform | None, pydantic.Field(description="The platform of the gather")]
    data_type: Annotated[
        DataType | None, pydantic.Field(description="The data type of the gather")
    ]
    source: Annotated[Source | None, pydantic.Field(description="The data type of the gather")]


class GatherResponse(GatherBase):
    """Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_id: int
    deleted_at: datetime.datetime | None = None


class GatherCreate(GatherBase):
    """Gather create schema.

    Properties to receive via API on creation.
    """


class GatherUpdate(pydantic.BaseModel):
    """Gather update schema."""
