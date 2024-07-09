"""Schemas for the projects."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic

from phiphi.api.projects.job_runs import schemas as job_runs_schemas


class ExpectedUsage(str, Enum):
    """Expected usage enum."""

    one_off = "one_off"
    weekly = "weekly"
    monthly = "monthly"


pi_delete_pydantic_field = pydantic.Field(
    default=183, description="PI deletion time in days, min 1, max 365", gt=1, lt=365
)
delete_after_days_field = pydantic.Field(
    default=183, description="Deletion time in days, min 1, max 365", gt=1, lt=365
)
workspace_slug_field = pydantic.Field(
    default="main", description="The workspace slug of the project"
)


class ProjectBase(pydantic.BaseModel):
    """Project base schema.

    Shared properties of all projects.
    """

    name: Annotated[str, pydantic.Field(description="The name of the project")]
    description: Annotated[str, pydantic.Field(description="The description of the project")]
    workspace_slug: Annotated[str, workspace_slug_field]

    pi_deleted_after_days: Annotated[int, pi_delete_pydantic_field]
    delete_after_days: Annotated[int, delete_after_days_field]
    expected_usage: Annotated[
        ExpectedUsage, pydantic.Field(description="The workspace expected usage of the project")
    ]
    dashboard_id: Annotated[
        int | None, pydantic.Field(description="The dashboard id of the project")
    ] = None


class ProjectCreate(ProjectBase):
    """Project create schema.

    Properties to receive via API on creation.
    """


class ProjectResponse(ProjectBase):
    """Project schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_job_run_completed_at: datetime.datetime | None
    latest_job_run: job_runs_schemas.JobRunResponse | None = None
    checked_problem_statement: bool = False
    checked_sources: bool = False
    checked_gather: bool = False
    checked_classify: bool = False
    checked_visualise: bool = False
    checked_explore: bool = False


class ProjectListResponse(ProjectBase):
    """Project List schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProjectUpdate(pydantic.BaseModel):
    """Project update schema."""

    name: str | None = None
    description: str | None = None
    pi_deleted_after_days: Annotated[int | None, pi_delete_pydantic_field]
    delete_after_days: Annotated[int | None, delete_after_days_field]
    expected_usage: ExpectedUsage | None = None
    workspace_slug: Annotated[str | None, workspace_slug_field]
    dashboard_id: int | None = None
    checked_problem_statement: bool = False
    checked_sources: bool = False
    checked_gather: bool = False
    checked_classify: bool = False
    checked_visualise: bool = False
    checked_explore: bool = False
