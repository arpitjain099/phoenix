"""Schemas for the instances."""
import datetime
from enum import Enum
from typing import Annotated

import pydantic


class EnvironmentKey(str, Enum):
    """Environment key enum."""

    main = "main"


class ExpectedUsage(str, Enum):
    """Expected usage enum."""

    one_off = "one_off"
    weekly = "weekly"
    monthly = "monthly"


class InstanceBase(pydantic.BaseModel):
    """Instance base schema.

    Shared properties of all instances.
    """

    name: Annotated[str, pydantic.Field(description="The name of the instance")]
    description: Annotated[str, pydantic.Field(description="The description of the instance")]
    environment_id: Annotated[
        EnvironmentKey,
        pydantic.Field(default="main", description="The environment key of the instance"),
    ]

    pi_deleted_after_days: Annotated[
        int,
        pydantic.Field(
            default=183, description="PI deletion time in days, min 1, max 365", gt=1, lt=365
        ),
    ]
    delete_after_days: Annotated[
        int,
        pydantic.Field(
            default=183, description="Deletion time in days, min 1, max 365", gt=1, lt=365
        ),
    ]
    expected_usage: Annotated[
        ExpectedUsage, pydantic.Field(description="The environment expected usage of the instance")
    ]


class InstanceCreate(InstanceBase):
    """Instance create schema.

    Properties to receive via API on creation.
    """


class Instance(InstanceBase):
    """Instance schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class InstanceUpdate(pydantic.BaseModel):
    """Instance update schema."""

    name: str | None = None
    description: str | None = None
    pi_deleted_after_days: int | None = None
    delete_after_days: int | None = None
    expected_usage: ExpectedUsage | None = None
    environment_id: str | None = None
