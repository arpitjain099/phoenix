"""Classifier Response schemas.

This copies ideas from Pydantic discriminator:
https://docs.pydantic.dev/latest/concepts/unions/#nested-discriminated-unions
"""
import datetime
from typing import Annotated, Optional, Union

import pydantic

from phiphi.api.projects.classifiers import base_schemas
from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas
from phiphi.api.projects.job_runs import schemas as job_runs_schemas

ClassifierDetail = Annotated[
    Union[keyword_match_schemas.KeywordMatchClassifierDetail],
    # This tells pydantic to use the `type` field to determine the type of the response
    # and optimises the Union
    pydantic.Field(description="Any classifier response", discriminator="type"),
]

classifier_detail_adapter = pydantic.TypeAdapter(ClassifierDetail)


class ClassifierSummary(base_schemas.ClassifierResponseBase):
    """Classifier Summary.

    Properties to return to client for a request like list the classifiers.

    Can be used to get a summary of the classifier.

    We are not using a union of sub classifiers because it improves speed and the strong typing of
    the latest_version is not needed.
    """

    archived_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_edited_at: Optional[datetime.datetime]
    latest_job_run: job_runs_schemas.JobRunResponse | None = None


ClassifierPipeline = Annotated[
    Union[keyword_match_schemas.KeywordMatchClassifierPipeline],
    pydantic.Field(description="Any classifier response", discriminator="type"),
]

classifier_pipeline_adapter = pydantic.TypeAdapter(ClassifierPipeline)
