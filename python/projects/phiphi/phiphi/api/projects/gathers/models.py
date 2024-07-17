"""Gather Models."""
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm

from phiphi import platform_db
from phiphi.api import base_models
from phiphi.api.projects.job_runs import models as job_run_models
from phiphi.api.projects.job_runs import schemas as job_run_schemas


class GatherBase(platform_db.Base):
    """Gather model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    project_id: orm.Mapped[int]
    source: orm.Mapped[str]
    platform: orm.Mapped[str]
    data_type: orm.Mapped[str]
    child_type: orm.Mapped[str]
    # In general we don't use foreign keys, but in this case it seemed appropriate
    delete_job_run_id: orm.Mapped[Optional[int]] = orm.mapped_column(sa.ForeignKey("job_runs.id"))


job_run_foreign_type_query = (
    f"JobRuns.foreign_job_type=='{job_run_schemas.ForeignJobType.gather.value}'"
)

class Gather(GatherBase, base_models.TimestampModel):
    """Gather model that can inherit from multiple models."""

    __tablename__ = "gathers"
    __mapper_args__ = {
        "polymorphic_identity": "gather",
        "polymorphic_on": "child_type",
    }

    # Relationships have to be on non abstract model.
    delete_job_run: orm.Mapped[job_run_models.JobRuns] = orm.relationship("JobRuns")

    # Relationship to get all related JobRuns, ordered by id descending
    job_runs = orm.relationship(
        "JobRuns",
        order_by="desc(JobRuns.id)",
        primaryjoin=(
            f"and_({job_run_foreign_type_query}, foreign(JobRuns.foreign_id)==Gather.id)"
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
