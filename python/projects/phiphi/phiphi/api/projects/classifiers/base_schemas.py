"""Base Schemas for classifiers."""
import datetime
from enum import Enum
from typing import Annotated, Any, Optional

import pydantic


class ClassifierType(str, Enum):
    """Classifier type enum."""

    keyword_match = "keyword_match"


class IntermediatoryClassBase(pydantic.BaseModel):
    """Class schema."""

    name: str
    description: str


class IntermediatoryClassCreate(IntermediatoryClassBase):
    """Class create schema."""


class IntermediatoryClassResponse(IntermediatoryClassBase):
    """Class response schema."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


ClassName = str
ClassDescription = str

ClassesDictType = Annotated[
    dict[ClassName, ClassDescription],
    pydantic.Field(
        description="The classes dictionary of the Classifier",
        examples=[{"class1": "class1 description", "class2": "class2 description"}],
    ),
]


class ClassifierCreate(pydantic.BaseModel):
    """Classifier create schema.

    Properties to receive via API on creation.

    This includes the intermediatory classes. That will be stored in `intermediatory_classes`
    table.

    No version of the classifier is created at this point, only the classifier itself.
    """

    name: Annotated[str, pydantic.Field(description="The name of the Classifier")]
    intermediatory_classes: list[IntermediatoryClassCreate]


class ClassifierVersionResponse(pydantic.BaseModel):
    """Classifier version schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    version_id: Annotated[
        int, pydantic.Field(description="The ID of this version (of the corresponding Classifier)")
    ]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    classes_dict: ClassesDictType
    # Typed as Any as the subclasses will define the params
    params: Annotated[Any, pydantic.Field(description="The params of the Classifier")]


class ClassifierResponseBase(pydantic.BaseModel):
    """Classifier schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    type: ClassifierType
    archived_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    intermediatory_classes: list[IntermediatoryClassResponse]
    # It is possible to have a classifier without any versions
    # This then uses the intermediatory tables to store data about the version
    latest_version: Annotated[
        Optional[ClassifierVersionResponse],
        pydantic.Field(description="The latest version of the Classifier", default=None),
    ]
