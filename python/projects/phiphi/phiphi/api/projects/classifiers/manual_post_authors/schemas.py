"""Manual posts authors schemas."""
import datetime
from typing import Literal, Optional

import pydantic

from phiphi.api.projects.classifiers import base_schemas


class IntermediatoryAuthorClassCreate(pydantic.BaseModel):
    """Intermediatory author classe create schema."""

    class_id: int
    phoenix_platform_message_author_id: str


class IntermediatoryAuthorClassResponse(IntermediatoryAuthorClassCreate):
    """Intermediatory authors class response schema."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    classifier_id: int
    class_name: str
    created_at: datetime.datetime
    # We don't return the updated at as classified_post_authors should not be updated.


class AuthorResponse(pydantic.BaseModel):
    """Author response schema."""

    phoenix_platform_message_author_id: str
    pi_platform_message_author_id: Optional[str]
    pi_platform_message_author_name: Optional[str]
    phoenix_processed_at: datetime.datetime
    platform: str
    post_count: int
    intermediatory_author_classes: list[IntermediatoryAuthorClassResponse] = []


class ManualPostAuthorsVersionBase(pydantic.BaseModel):
    """Manual post authors version base schema."""

    classes: list[base_schemas.ClassLabel]
    # TODO: define the type of this
    params: dict


class ManualPostAuthorsVersionResponse(
    ManualPostAuthorsVersionBase, base_schemas.ClassifierVersionResponse
):
    """Manual post authors version schema."""


class ManualPostAuthorsClassifierResponse(base_schemas.ClassifierResponseBase):
    """Manual post authors classifier response."""

    # This seems to be the correct way to do this:
    # https://github.com/pydantic/pydantic/issues/8708
    type: Literal[base_schemas.ClassifierType.manual_post_authors]
    latest_version: Optional[ManualPostAuthorsVersionResponse] = None


class ManualPostAuthorsClassifierDetail(
    ManualPostAuthorsClassifierResponse, base_schemas.ClassifierDetailBase
):
    """Manual post authors classifier response."""

    intermediatory_author_classes: list[IntermediatoryAuthorClassResponse] = []
