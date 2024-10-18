"""Manual posts authors schemas."""
from typing import Literal, Optional

import pydantic

from phiphi.api.projects.classifiers import base_schemas


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
