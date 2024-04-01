"""Schemas for the instances."""
import datetime

import pydantic


class InstanceBase(pydantic.BaseModel):
    """Instance base schema.

    Shared properties of all instances.
    """

    name: str | None = None
    description: str | None = None
    environment_key: str | None = None
    pi_deleted_after: int | None = None
    deleted_after: int | None = None
    expected_usage: str | None = None


class InstanceCreate(InstanceBase):
    """Instance create schema.

    Properties to receive via API on creation.
    """

    name: str | None = None
    description: str | None = None
    pi_deleted_after: int | None = None
    deleted_after: int | None = None
    expected_usage: str | None = None


class Instance(InstanceBase):
    """Instance schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime


class InstanceUpdate(pydantic.BaseModel):
    """Instance update schema."""

    name: str | None = None
    description: str | None = None
    pi_deleted_after: int | None = None
    deleted_after: int | None = None
    expected_usage: str | None = None
