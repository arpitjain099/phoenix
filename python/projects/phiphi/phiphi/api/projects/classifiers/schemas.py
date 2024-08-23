"""Schemas for classifiers."""
from datetime import datetime
from enum import Enum
from typing import Annotated, Union

import pydantic


class ClassifierType(str, Enum):
    """Classifier type enum."""

    keyword_match = "keyword_match"


class ClassToKeywordConfig(pydantic.BaseModel):
    """Class to keyword config containing keyword matches."""

    class_id: int
    musts: Annotated[
        str,
        pydantic.Field(
            description="Whitespace separated list of keywords that must all match to classify "
            "as this class"
        ),
    ]
    # These are optional upgrades which are not going to be implemented in the first version
    # shoulds: Annotated[str, pydantic.Field(description="Whitespace separated list of keywords
    # of which one must match to classify as this class")]
    # nots: Annotated[str, pydantic.Field(description="Whitespace separated list of keywords
    #     of which none can match to classify as this class")]


class KeywordMatchParams(pydantic.BaseModel):
    """Params subschema for keyword match classifier."""

    class_to_keyword_configs: list[ClassToKeywordConfig]


class ClassifierBase(pydantic.BaseModel):
    """Classifier base schema.

    Shared properties of all classifier schemas.
    """

    project_id: Annotated[
        int, pydantic.Field(description="The ID of the project which the Classifier is within")
    ]
    name: Annotated[str, pydantic.Field(description="The name of the Classifier")]
    type: Annotated[ClassifierType, pydantic.Field(description="The type of the classifier")]
    params: Annotated[
        Union[dict, KeywordMatchParams], pydantic.Field(description="The params of the Classifier")
    ]


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
    updated_at: datetime
    archived_at: datetime | None


class ClassifierArchive(pydantic.BaseModel):
    """Classifier archive schema."""


class ClassifierKeywordMatchResponse(ClassifierResponse):
    """Keyword match classifier schema.

    Properties to return to client.
    """

    params: KeywordMatchParams


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
    created_at: datetime
    updated_at: datetime


class ClassUpdate(pydantic.BaseModel):
    """Class update schema."""

    name: str | None = None
    description: str | None = None


class ClassDelete(pydantic.BaseModel):
    """Class delete schema."""
