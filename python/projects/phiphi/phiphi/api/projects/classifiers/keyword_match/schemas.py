"""Keyword Match Schemas."""
import datetime
from typing import Annotated, Literal, Optional

import pydantic
from pydantic.functional_validators import AfterValidator
from typing_extensions import TypedDict

from phiphi.api.projects.classifiers import base_schemas

MUSTS_DESCRIPTION = (
    "Whitespace separated list of keywords that must all match to classify as this class"
)
NOTS_DESCRIPTION = (
    "Whitespace separated list of keywords of which none can match to classify as this class"
)


def empty_string_to_none(value: str) -> Optional[str]:
    """Convert empty string to None."""
    return None if value == "" else value


class IntermediatoryClassToKeywordConfigCreate(pydantic.BaseModel):
    """Intermediatory class to keyword config create schema."""

    class_id: int
    musts: Annotated[str, pydantic.Field(description=MUSTS_DESCRIPTION)]
    nots: Annotated[
        Optional[str],
        pydantic.Field(description=NOTS_DESCRIPTION, default=None),
        # Nots can be "" if from the orm. If a create was done with an empty `nots` then this wil
        # be persisted in the database as "". This is being converted to None here to normalise it
        # in to the expected value.
        AfterValidator(empty_string_to_none),
    ]


class IntermediatoryClassToKeywordConfigResponse(IntermediatoryClassToKeywordConfigCreate):
    """Intermediatory class to keyword config response schema."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class_name: str


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
