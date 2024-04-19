"""Schemas for project runs."""
import datetime
from enum import Enum

import pydantic


class RunStatus(str, Enum):
    """Project run status."""

    in_queue = "in_queue"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    yet_to_run = "yet_to_run"


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
    run_status: str


class ProjectRunsUpdate(pydantic.BaseModel):
    """Project runs update schema."""

    started_processing_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    failed_at: datetime.datetime | None = None
