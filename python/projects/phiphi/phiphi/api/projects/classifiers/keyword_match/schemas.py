"""Keyword Match Schemas."""
import datetime
from typing import Annotated, Literal, Optional

import pydantic
from typing_extensions import TypedDict

from phiphi.api.projects.classifiers import base_schemas

MUSTS_DESCRIPTION = (
    "Whitespace separated list of keywords that must all match to classify as this class"
)
NOTS_DESCRIPTION = (
    "Whitespace separated list of keywords; "
    "to be classified into this class, it must not contain any of the words"
)


class IntermediatoryClassToKeywordConfigCreate(pydantic.BaseModel):
    """Intermediatory class to keyword config create schema."""

    class_id: int
    musts: Annotated[str, pydantic.Field(description=MUSTS_DESCRIPTION)]
    nots: Annotated[
        Optional[str],
        pydantic.Field(description=NOTS_DESCRIPTION, default=""),
    ]


class IntermediatoryClassToKeywordConfigPatch(pydantic.BaseModel):
    """Intermediatory class to keyword config patch schema."""

    musts: Annotated[Optional[str], pydantic.Field(description=MUSTS_DESCRIPTION, default=None)]
    nots: Annotated[
        Optional[str],
        pydantic.Field(description=NOTS_DESCRIPTION, default=None),
    ]


class IntermediatoryClassToKeywordConfigResponse(IntermediatoryClassToKeywordConfigCreate):
    """Intermediatory class to keyword config response schema."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class_name: str
    # Class description is added as this makes the UI for the console to compute easier
    class_description: str


class ClassToKeywordConfig(TypedDict):
    """Class to keyword config containing keyword matches.

    This is a TypedDict rather then a pydantic models as fast api recommends using TypedDict for
    nested objects to improve performance.
    https://docs.pydantic.dev/latest/concepts/performance/#use-typeddict-over-nested-models
    """

    class_name: str
    musts: Annotated[
        str,
        pydantic.Field(
            description=MUSTS_DESCRIPTION,
        ),
    ]
    nots: Annotated[Optional[str], pydantic.Field(description=NOTS_DESCRIPTION, default="")]


class KeywordMatchParams(TypedDict):
    """Params subschema for keyword match classifier.

    This is a TypedDict rather then a pydantic models as fast api recommends using TypedDict for
    nested objects to improve performance.
    https://docs.pydantic.dev/latest/concepts/performance/#use-typeddict-over-nested-models
    """

    class_to_keyword_configs: list[ClassToKeywordConfig]


class KeywordMatchVersionBase(pydantic.BaseModel):
    """Keyword match version base schema."""

    classes: list[base_schemas.ClassLabel]
    params: KeywordMatchParams


class KeywordMatchVersionResponse(KeywordMatchVersionBase, base_schemas.ClassifierVersionResponse):
    """Keyword match version schema."""


class KeywordMatchClassifierResponse(base_schemas.ClassifierResponseBase):
    """Keyword match classifier response."""

    # This seems to be the correct way to do this:
    # https://github.com/pydantic/pydantic/issues/8708
    type: Literal[base_schemas.ClassifierType.keyword_match]
    latest_version: Optional[KeywordMatchVersionResponse] = None


class KeywordMatchClassifierDetail(
    KeywordMatchClassifierResponse, base_schemas.ClassifierDetailBase
):
    """Keyword match classifier response."""

    intermediatory_class_to_keyword_configs: list[IntermediatoryClassToKeywordConfigResponse] = []


class KeywordMatchClassifierPipeline(
    KeywordMatchClassifierResponse, base_schemas.ClassifierPipelineBase
):
    """Keyword match classifier response."""

    latest_version: KeywordMatchVersionResponse
