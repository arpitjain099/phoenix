"""Schemas for classifiers."""
from typing import Annotated

import pydantic


class ClassifierBase(pydantic.BaseModel):
    """Classifier base schema.

    Shared properties of all classifier schemas.
    """

    project_id: Annotated[
        int, pydantic.Field(description="The ID of the project which the Classifier is within")
    ]
    name: Annotated[str, pydantic.Field(description="The name of the Classifier")]
    type: Annotated[str, pydantic.Field(description="The type of the Classifier")]
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
    deleted: bool


class ClassifierDelete(pydantic.BaseModel):
    """Classifier delete schema."""

    id: int
