"""Instance runs model."""
import datetime
from typing import Optional

from phiphi import platform_db
from phiphi.api import base_models
from sqlalchemy import orm


class InstanceRunsBase(platform_db.Base):
    """Instance Runs Model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    instance_id: orm.Mapped[int]
    started_processing_at: orm.Mapped[Optional[datetime.datetime]]
    environment_slug: orm.Mapped[str]
    completed_at: orm.Mapped[Optional[datetime.datetime]]
    failed_at: orm.Mapped[Optional[datetime.datetime]]


class InstanceRuns(InstanceRunsBase, base_models.TimestampModel):
    """Instance runs model that can inherit from multiple models."""

    __tablename__ = "instance_runs"
