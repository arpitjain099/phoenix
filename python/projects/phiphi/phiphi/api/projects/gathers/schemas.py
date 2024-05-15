"""Schemas for gathers."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic
from phiphi.api import base_schemas


class Platform(str, Enum):
    """Platform enum."""

    facebook = "facebook"


class DataType(str, Enum):
    """data type enum."""

    posts = "posts"
    comments = "comments"


class Source(str, Enum):
    """source enum."""

    apify = "apify"


class GatherBase(pydantic.BaseModel):
    """Gather base schema.

    Shared properties of all gathers.

    Please note that the source, platform and data type are not included in this schema as they are
    taken from the route that creates the child gather. This is because the source, platform and
    data type are part of the child type and are not user defined.
    """

    description: Annotated[str, pydantic.Field(description="The description of the gather")]


class GatherResponse(GatherBase):
    """Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int
    platform: Annotated[Platform, pydantic.Field(description="The platform of the gather")]
    data_type: Annotated[DataType, pydantic.Field(description="The data type of the gather")]
    source: Annotated[Source, pydantic.Field(description="The data type of the gather")]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_id: int
    deleted_at: datetime.datetime | None = None
    run_status: base_schemas.RunStatus = base_schemas.RunStatus.yet_to_run


class GatherCreate(GatherBase):
    """Gather create schema.

    Properties to receive via API on creation.
    """


class GatherUpdate(pydantic.BaseModel):
    """Gather update schema."""


class GatherEstimate(pydantic.BaseModel):
    """Gather estimate schema."""

    id: int
    estimated_credit_cost: int
    estimated_credit_cumulative_cost: int
    estimated_duration_minutes: int
