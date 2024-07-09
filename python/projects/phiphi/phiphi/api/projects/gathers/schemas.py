"""Schemas for gathers."""
import datetime
from enum import Enum
from typing import Annotated, Any, Dict

import pydantic

from phiphi.api.projects.job_runs import schemas as job_runs_schemas


class ChildTypeName(str, Enum):
    """Child Type Enum.

    Additions to this enum should be reflected in the CHILD_TYPES_MAP in child_types.py file.
    """

    apify_facebook_posts = "apify_facebook_posts"
    apify_facebook_comments = "apify_facebook_comments"


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

    name: Annotated[str, pydantic.Field(description="The name of the gather")]


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
    latest_job_run: job_runs_schemas.JobRunResponse | None = None
    child_type: Annotated[
        ChildTypeName, pydantic.Field(description="The child type of the gather")
    ]

    def serialize_to_apify_input(self) -> Dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        instance_dict = self.model_dump(by_alias=True, exclude_unset=True)
        apify_dict = {
            key: value for key, value in instance_dict.items() if key not in self.model_fields_set
        }
        return apify_dict


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
    estimated_duration_minutes: int
