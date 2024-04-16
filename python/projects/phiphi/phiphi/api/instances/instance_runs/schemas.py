"""Schemas for instance runs."""
import datetime

import pydantic


class InstanceRunsBase(pydantic.BaseModel):
    """Instance runs base schema.

    Shared properties of all gathers.
    """


class InstanceRunsResponse(InstanceRunsBase):
    """Instance runs schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    instance_id: int
    start_processing_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    failed_at: datetime.datetime | None = None
    environment_slug: str
