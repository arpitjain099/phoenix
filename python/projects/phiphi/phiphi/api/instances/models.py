"""Instance Models."""
from typing import Optional, cast

from sqlalchemy import ForeignKey, orm
from sqlalchemy.ext.hybrid import hybrid_property

from phiphi import platform_db
from phiphi.api import base_models
from phiphi.api.instances.instance_runs import models


class InstanceBase(platform_db.Base):
    """Instance Model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    description: orm.Mapped[str]
    environment_slug: orm.Mapped[str] = orm.mapped_column(
        ForeignKey("environments.slug"), default="main"
    )
    pi_deleted_after_days: orm.Mapped[int]
    delete_after_days: orm.Mapped[int]
    expected_usage: orm.Mapped[Optional[str]]


class Instance(InstanceBase, base_models.TimestampModel):
    """Instance model that can inherit from multiple models."""

    __tablename__ = "instances"

    # Relationship to get all related InstanceRuns, ordered by created_at descending
    instance_runs = orm.relationship(
        "InstanceRuns",
        order_by="desc(InstanceRuns.created_at)",
        primaryjoin="Instance.id == InstanceRuns.instance_id",
        lazy="dynamic",
    )

    @hybrid_property
    def last_run(self) -> models.InstanceRuns:
        """Property to get the most recent InstanceRun."""
        last_run = self.instance_runs.first()

        return cast(models.InstanceRuns, last_run)

    @hybrid_property
    def run_status(self) -> str:
        """Run status hybrid property."""
        # Check if there are any running instance runs
        status = self.last_run.run_status
        return str(status)
