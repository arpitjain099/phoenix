"""Schemas for job_runs."""
from datetime import datetime
from enum import Enum
from typing import Optional

import pydantic


class Status(str, Enum):
    """Job run status."""

    awaiting_start = "awaiting_start"
    processing = "processing"
    completed_sucessfully = "completed_sucessfully"
    failed = "failed"


class JobRunCreate(pydantic.BaseModel):
    """Schema for creating a job run."""

    foreign_id: int = pydantic.Field(
        ..., description="The foreign table ID associated with this job run"
    )
    foreign_job_type: str = pydantic.Field(
        ..., description="The type of job (gather, classify, etc.)"
    )
    prefect_outer_flow_run_id: str = pydantic.Field(
        ..., description="The ID of the outer flow run from Prefect"
    )
    prefect_outer_flow_run_name: str = pydantic.Field(
        ..., description="The name of the outer flow run from Prefect"
    )


class JobRunCreated(pydantic.BaseModel):
    """Schema for the response when a job run is created."""

    id: int = pydantic.Field(..., description="The ID of the newly created job run")


class JobRunStarted(pydantic.BaseModel):
    """Schema for updating a job run when it starts."""

    id: int = pydantic.Field(..., description="The ID of the job run being updated")
    prefect_inner_flow_run_id: str = pydantic.Field(
        ..., description="The ID of the inner flow run from Prefect"
    )
    prefect_inner_flow_run_name: str = pydantic.Field(
        ..., description="The name of the inner flow run from Prefect"
    )
    prefect_inner_flow_run_status: Status = pydantic.Field(
        default=Status.processing, description="The status of the inner flow run"
    )
    prefect_inner_flow_run_started_at: datetime = pydantic.Field(
        default_factory=datetime.now, description="The start time of the inner flow run"
    )


class JobRunCompleted(pydantic.BaseModel):
    """Schema for updating a job run when it completes."""

    id: int = pydantic.Field(..., description="The ID of the job run being updated")
    prefect_inner_flow_run_status: Status = pydantic.Field(
        ..., description="The final status of the inner flow run"
    )
    prefect_inner_flow_run_completed_at: Optional[datetime] = pydantic.Field(
        default_factory=datetime.now, description="The completion time of the inner flow run"
    )
