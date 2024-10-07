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

    class_name: str
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


class ClassifierVersion(pydantic.BaseModel):
    """Classifier version base schema.

    Shared properties of all classifier version schemas.
    """

    classes_dict: Annotated[
        dict, pydantic.Field(description="The classes dictionary of the Classifier")
    ]
    params: Annotated[
        Union[dict, KeywordMatchParams], pydantic.Field(description="The params of the Classifier")
    ]


class ClassifierVersionCreate(ClassifierVersion):
    """Classifier version create schema.

    Properties to receive via API on creation.
    """


class ClassifierVersionResponse(ClassifierVersion):
    """Classifier version schema.

    Properties to return to client.
    """

    version_id: Annotated[
        int,
        pydantic.Field(description="The ID of this version (of the corresponding Classifier)"),
    ]
    classifier_id: Annotated[
        int, pydantic.Field(description="The ID of the Classifier this is a version of")
    ]
    created_at: datetime
    updated_at: datetime


class ClassifierBase(pydantic.BaseModel):
    """Classifier base schema.

    Shared properties of all classifier schemas.
    """

    project_id: Annotated[
        int, pydantic.Field(description="The ID of the project which the Classifier is within")
    ]
    name: Annotated[str, pydantic.Field(description="The name of the Classifier")]
    type: Annotated[ClassifierType, pydantic.Field(description="The type of the Classifier")]


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
    latest_version: Annotated[
        ClassifierVersionResponse,
        pydantic.Field(description="The latest version of the Classifier"),
    ]


class ClassifierArchive(pydantic.BaseModel):
    """Classifier archive schema."""


class ClassifierKeywordMatchVersionResponse(ClassifierVersionResponse):
    """Keyword match classifier schema.

    Properties to return to client.
    """

    params: KeywordMatchParams


class ClassifierKeywordMatchResponse(ClassifierResponse):
    """Keyword match classifier schema.

    Properties to return to client.
    """

    latest_version: ClassifierKeywordMatchVersionResponse
