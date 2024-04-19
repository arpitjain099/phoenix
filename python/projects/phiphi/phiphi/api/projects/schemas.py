"""Schemas for the projects."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic


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
environment_slug_field = pydantic.Field(
    default="main", description="The environment id of the project"
)


class ProjectBase(pydantic.BaseModel):
    """Project base schema.

    Shared properties of all projects.
    """

    name: Annotated[str, pydantic.Field(description="The name of the project")]
    description: Annotated[str, pydantic.Field(description="The description of the project")]
    environment_slug: Annotated[str, environment_slug_field]

    pi_deleted_after_days: Annotated[int, pi_delete_pydantic_field]
    delete_after_days: Annotated[int, delete_after_days_field]
    expected_usage: Annotated[
        ExpectedUsage, pydantic.Field(description="The environment expected usage of the project")
    ]


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
    run_status: str | None = None


class ProjectUpdate(pydantic.BaseModel):
    """Project update schema."""

    name: str | None = None
    description: str | None = None
    pi_deleted_after_days: Annotated[int | None, pi_delete_pydantic_field]
    delete_after_days: Annotated[int | None, delete_after_days_field]
    expected_usage: ExpectedUsage | None = None
    environment_slug: Annotated[str | None, environment_slug_field]
