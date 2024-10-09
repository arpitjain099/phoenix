"""Base Schemas for classifiers."""
import datetime
from enum import Enum
from typing import Annotated, Any, Optional

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


class ClassifierVersionResponse(pydantic.BaseModel):
    """Classifier version schema.

    Properties to return to client.
    """

    version_id: Annotated[
        int, pydantic.Field(description="The ID of this version (of the corresponding Classifier)")
    ]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    classes_dict: ClassesDictType
    # Typed as Any as the subclasses will define the params
    params: Annotated[Any, pydantic.Field(description="The params of the Classifier")]
    model_config = pydantic.ConfigDict(from_attributes=True)


class ClassifierResponse(pydantic.BaseModel):
    """Classifier schema.

    Properties to return to client.
    """

    id: int
    project_id: int
    name: str
    type: ClassifierType
    archived_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = pydantic.ConfigDict(from_attributes=True)
    latest_version: ClassifierVersionResponse
