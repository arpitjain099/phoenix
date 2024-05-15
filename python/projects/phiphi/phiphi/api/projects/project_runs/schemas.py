"""Schemas for project runs."""
import datetime

import pydantic
from phiphi.api import base_schemas


class ProjectRunsBase(pydantic.BaseModel):
    """Project runs base schema.

    Shared properties of all gathers.
    """


class ProjectRunsResponse(ProjectRunsBase):
    """Project runs schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    project_id: int
    started_processing_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    failed_at: datetime.datetime | None = None
    environment_slug: str
    run_status: base_schemas.RunStatus


class ProjectRunsUpdate(pydantic.BaseModel):
    """Project runs update schema."""

    started_processing_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    failed_at: datetime.datetime | None = None
