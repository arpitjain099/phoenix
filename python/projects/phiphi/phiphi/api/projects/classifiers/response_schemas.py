"""Classifier Response schemas.

This copies ideas from Pydantic discriminator:
https://docs.pydantic.dev/latest/concepts/unions/#nested-discriminated-unions
"""
from typing import Annotated, Union

import pydantic

from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas

AnyClassifierResponse = Annotated[
    Union[keyword_match_schemas.KeywordMatchClassifierResponse],
    # This tells pydantic to use the `type` field to determine the type of the response
    # and optimises the Union
    pydantic.Field(description="Any classifier response", discriminator="type"),
]

classifier_response_adaptor = pydantic.TypeAdapter(AnyClassifierResponse)
