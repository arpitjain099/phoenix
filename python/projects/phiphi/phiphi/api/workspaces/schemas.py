"""Schemas for the environments."""
import datetime
from typing import Annotated

import pydantic


class EnvironmentBase(pydantic.BaseModel):
    """Environment base schema.

    Shared properties of all environment schemas.
    """

    description: Annotated[str, pydantic.Field(description="The description of the Environment")]
    name: Annotated[str, pydantic.Field(description="The name of the Environment")]
    slug: Annotated[str, pydantic.Field(description="The slug of the Environment")]


class EnvironmentCreate(EnvironmentBase):
    """Environment create schema.

    Properties to receive via API on creation.
    """


class EnvironmentResponse(EnvironmentBase):
    """Environment schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    slug: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class EnvironmentUpdate(pydantic.BaseModel):
    """Environment update schema."""

    name: str | None = None
    description: str | None = None
    slug: str | None = None


class SlugResponse(pydantic.BaseModel):
    """Environment unique slug."""

    slug: str
