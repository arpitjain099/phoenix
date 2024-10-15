"""Schemas for job_runs."""
from datetime import datetime
from enum import Enum
from typing import Optional

import pydantic


class Status(str, Enum):
    """Job run status."""

    awaiting_start = "awaiting_start"
    in_queue = "in_queue"
    processing = "processing"
    completed_successfully = "completed_successfully"
    failed = "failed"


class ForeignJobType(str, Enum):
    """The type of job run.

    These job types correspond to the different types of pipeline jobs/prefect flows that can be
    run.

    See flow_runner_flow.py for the corresponding flows.
    """

    gather = "gather"
    delete_gather = "delete_gather"
    classify = "classify"
    tabulate = "tabulate"
    gather_classify_tabulate = "gather_classify_tabulate"
    classify_tabulate = "classify_tabulate"
    delete_gather_tabulate = "delete_gather_tabulate"
    classifier_archive = "classifier_archive"
    classifier_restore = "classifier_restore"


class JobRunCreate(pydantic.BaseModel):
    """Schema for creating a job run."""

    foreign_id: int = pydantic.Field(
        ..., description="The foreign table ID associated with this job run"
    )
    foreign_job_type: ForeignJobType = pydantic.Field(..., description="The type of job")


class JobRunCreated(pydantic.BaseModel):
    """Schema for the response when a job run is created."""

    id: int = pydantic.Field(..., description="The ID of the newly created job run")


class JobRunUpdateStarted(pydantic.BaseModel):
    """Schema for updating a job run when it starts."""

    id: int = pydantic.Field(..., description="The ID of the job run being updated")
    flow_run_id: str = pydantic.Field(..., description="The ID of the flow run from Prefect")
    flow_run_name: str = pydantic.Field(..., description="The name of the flow run from Prefect")
    status: Status = pydantic.Field(
        default=Status.in_queue, description="The status of the flow run"
    )


class JobRunUpdateProcessing(pydantic.BaseModel):
    """Schema for updating a job run when it is processing."""

    id: int = pydantic.Field(..., description="The ID of the job run being updated")
    status: Status = pydantic.Field(
        default=Status.processing, description="The status of the flow run"
    )
    started_processing_at: datetime = pydantic.Field(
        default_factory=datetime.now, description="The start time of the flow run"
    )


class JobRunUpdateCompleted(pydantic.BaseModel):
    """Schema for updating a job run when it completes, or fails."""

    id: int = pydantic.Field(..., description="The ID of the job run being updated")
    status: Status = pydantic.Field(..., description="The final status of the flow run")
    completed_at: Optional[datetime] = pydantic.Field(
        default_factory=datetime.now, description="The completion, or fail time of the flow run"
    )


class JobRunResponse(JobRunCreated, JobRunCreate):
    """Schema for job_run response - uses optional fields to cover all possible responses."""

    # To map from the JobRuns model
    model_config = pydantic.ConfigDict(from_attributes=True)

    created_at: datetime = pydantic.Field(
        default_factory=datetime.now, description="The time the job run was created"
    )
    updated_at: datetime = pydantic.Field(
        default_factory=datetime.now, description="The time the job run was last updated"
    )
    project_id: int = pydantic.Field(
        ..., description="The ID of the project associated with this job run"
    )
    status: Status = pydantic.Field(..., description="The status of the job run")
    started_processing_at: Optional[datetime] = pydantic.Field(
        default=None, description="The start time of the flow run"
    )
    completed_at: Optional[datetime] = pydantic.Field(
        default=None, description="The completion time of the flow run"
    )
    flow_run_id: Optional[str] = pydantic.Field(
        default=None, description="The ID of the flow run from Prefect"
    )
    flow_run_name: Optional[str] = pydantic.Field(
        default=None, description="The name of the flow run from Prefect"
    )
