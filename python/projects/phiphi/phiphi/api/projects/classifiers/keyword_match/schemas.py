"""Keyword Match Schemas."""
from typing import Annotated, Literal, Optional

import pydantic
from typing_extensions import TypedDict

from phiphi.api.projects.classifiers import base_schemas


class ClassToKeywordConfig(TypedDict):
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


class KeywordMatchParams(TypedDict):
    """Params subschema for keyword match classifier."""

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
