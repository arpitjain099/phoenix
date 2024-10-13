"""Classifier Response schemas.

This copies ideas from Pydantic discriminator:
https://docs.pydantic.dev/latest/concepts/unions/#nested-discriminated-unions
"""
import datetime
from typing import Annotated, Optional, Union

import pydantic

from phiphi.api.projects.classifiers import base_schemas
from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas

Classifier = Annotated[
    Union[keyword_match_schemas.KeywordMatchClassifierResponse],
    # This tells pydantic to use the `type` field to determine the type of the response
    # and optimises the Union
    pydantic.Field(description="Any classifier response", discriminator="type"),
]

classifier_adapter = pydantic.TypeAdapter(Classifier)


class OptimisedClassifier(pydantic.BaseModel):
    """Optimised Classifier schema.

    Properties to return to client for a request like list the classifiers

    This is a simplified version of the ClassifierResponseBase schema. That allows for optimisation
    of the GET for all classifiers.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    type: base_schemas.ClassifierType
    archived_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    latest_version: Annotated[
        Optional[base_schemas.ClassifierVersionResponse],
        pydantic.Field(description="The latest version of the Classifier", default=None),
    ]
