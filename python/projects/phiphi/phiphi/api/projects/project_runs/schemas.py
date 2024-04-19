"""Schemas for instance runs."""
import datetime
from enum import Enum

import pydantic


class RunStatus(str, Enum):
    """Instance run status."""

    in_queue = "in_queue"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    yet_to_run = "yet_to_run"


class InstanceRunsBase(pydantic.BaseModel):
    """Instance runs base schema.

    Shared properties of all gathers.
    """


class InstanceRunsResponse(InstanceRunsBase):
    """Instance runs schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    instance_id: int
    started_processing_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    failed_at: datetime.datetime | None = None
    environment_slug: str
    run_status: str


class InstanceRunsUpdate(pydantic.BaseModel):
    """Instance runs update schema."""

    started_processing_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    failed_at: datetime.datetime | None = None
