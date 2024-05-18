"""Gather Models."""
import datetime
from typing import Optional

from phiphi import platform_db
from phiphi.api import base_models
from phiphi.api.projects.job_runs import models as job_run_models
from sqlalchemy import orm


class GatherBase(platform_db.Base):
    """Gather model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    description: orm.Mapped[str]
    project_id: orm.Mapped[int]
    source: orm.Mapped[str]
    platform: orm.Mapped[str]
    data_type: orm.Mapped[str]
    deleted_at: orm.Mapped[Optional[datetime.datetime]]
    child_type: orm.Mapped[str]


class Gather(GatherBase, base_models.TimestampModel):
    """Gather model that can inherit from multiple models."""

    __tablename__ = "gathers"
    __mapper_args__ = {
        "polymorphic_identity": "gather",
        "polymorphic_on": "child_type",
    }

    # Relationship to get all related JobRuns, ordered by id descending
    job_runs = orm.relationship(
        "JobRuns",
        order_by="desc(JobRuns.id)",
        primaryjoin=(
            "and_(JobRuns.foreign_job_type=='gather', foreign(JobRuns.foreign_id)==Gather.id)"
        ),
        lazy="dynamic",
    )

    @property
    def latest_job_run(self) -> job_run_models.JobRuns | None:
        """Property to get the most recent JobRun."""
        latest_run: job_run_models.JobRuns | None = self.job_runs.first()

        if latest_run is None:
            return None

        return latest_run
