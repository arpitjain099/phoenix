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
    apify_facebook_searches_posts = "apify_facebook_searches_posts"
    apify_facebook_comments = "apify_facebook_comments"
    apify_tiktok_hashtags_posts = "apify_tiktok_hashtags_posts"
    apify_tiktok_accounts_posts = "apify_tiktok_accounts_posts"
    apify_tiktok_searches_posts = "apify_tiktok_searches_posts"
    apify_tiktok_comments = "apify_tiktok_comments"


class Platform(str, Enum):
    """Platform enum."""

    facebook = "facebook"
    tiktok = "tiktok"


class DataType(str, Enum):
    """data type enum."""

    posts = "posts"
    comments = "comments"


class GatherBase(pydantic.BaseModel):
    """Gather base schema.

    Shared properties of all gathers.
    """

    name: Annotated[str, pydantic.Field(description="The name of the gather")]


class GatherResponse(GatherBase):
    """Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_id: int
    latest_job_run: job_runs_schemas.JobRunResponse | None = None
    delete_job_run: job_runs_schemas.JobRunResponse | None = None
    child_type: Annotated[
        ChildTypeName, pydantic.Field(description="The child type of the gather")
    ]

    def serialize_to_apify_input(self) -> Dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        # We exclude Nones because we believe Apify's Optional fields mean that they can be
        # omitted, not that they can be None.
        instance_dict = self.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)
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

    name: Annotated[str | None, pydantic.Field(default=None, description="The name of the gather")]

    class Config:
        """Config."""

        # Don't allow extra fields on the update so that if a user tries to update a field that is
        # not allowed they are given an error.
        extra = pydantic.Extra.forbid


class GatherEstimate(pydantic.BaseModel):
    """Gather estimate schema."""

    id: int
    estimated_credit_cost: int
    estimated_duration_minutes: int
