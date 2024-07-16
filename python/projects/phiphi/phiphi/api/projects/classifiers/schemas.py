"""Schemas for classifiers."""
from datetime import datetime
from enum import Enum
from typing import Annotated

import pydantic


class ClassifierType(str, Enum):
    """Classifier type enum."""

    keyword_match = "keyword_match"


class ClassifierBase(pydantic.BaseModel):
    """Classifier base schema.

    Shared properties of all classifier schemas.
    """

    project_id: Annotated[
        int, pydantic.Field(description="The ID of the project which the Classifier is within")
    ]
    classifier_name: Annotated[str, pydantic.Field(description="The name of the Classifier")]
    classifier_type: Annotated[
        ClassifierType, pydantic.Field(description="The type of the classifier")
    ]
    params: Annotated[dict, pydantic.Field(description="The params of the Classifier")]


class ClassifierCreate(ClassifierBase):
    """Classifier create schema.

    Properties to receive via API on creation.
    """


class ClassifierResponse(ClassifierBase):
    """Classifier schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    archived_at: datetime | None


class ClassifierArchive(pydantic.BaseModel):
    """Classifier archive schema."""


class ClassBase(pydantic.BaseModel):
    """Class base schema.

    Shared properties of all class schemas.
    """

    project_id: Annotated[
        int, pydantic.Field(description="The ID of the project the Class is within")
    ]
    name: Annotated[str, pydantic.Field(description="The name of the Class")]
    description: Annotated[str, pydantic.Field(description="The description of the Class")]


class ClassCreate(ClassBase):
    """Class create schema.

    Properties to receive via API on creation.
    """


class ClassResponse(ClassBase):
    """Class schema.

    Properties to return to client.
    """

    id: int


class ClassUpdate(pydantic.BaseModel):
    """Class update schema."""

    name: str | None = None
    description: str | None = None


class ClassDelete(pydantic.BaseModel):
    """Class delete schema."""
