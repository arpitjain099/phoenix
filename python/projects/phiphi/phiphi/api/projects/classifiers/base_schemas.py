"""Base Schemas for classifiers."""
from enum import Enum
from typing import Annotated, Any

import pydantic


class ClassifierType(str, Enum):
    """Classifier type enum."""

    keyword_match = "keyword_match"


# Currently these produces unhelpful example in the swagger docs but this is not a big deal
ClassesDictType = Annotated[
    dict[str, str], pydantic.Field(description="The classes dictionary of the Classifier")
]


class ClassifierVersionCreate(pydantic.BaseModel):
    """Classifier version create schema.

    Properties to receive via API on creation.
    """

    classes_dict: ClassesDictType
    # Any as these will be defined by subclasses
    params: Any


class ClassifierCreate(pydantic.BaseModel):
    """Classifier create schema.

    Properties to receive via API on creation.
    """

    name: Annotated[str, pydantic.Field(description="The name of the Classifier")]
    # For the create `version` is used over `latest_version` as on the create the version submitted
    # is the latest version
    version: ClassifierVersionCreate
