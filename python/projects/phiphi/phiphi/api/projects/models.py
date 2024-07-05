"""Project Models."""
import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Index, orm

from phiphi import platform_db
from phiphi.api import base_models
from phiphi.api.projects.job_runs import models as job_run_models


class ProjectBase(platform_db.Base):
    """Project Model."""

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
    deleted_at: orm.Mapped[Optional[datetime.datetime]]
    dashboard_id: orm.Mapped[Optional[int]]
    # Needs to be optional or problems with the database and we thought that this was better then
    # using a server_default=sa.sql.expression.false() in the migration.
    checked_problem_statement: orm.Mapped[Optional[bool]] = orm.mapped_column(default=False)
    checked_sources: orm.Mapped[Optional[bool]] = orm.mapped_column(default=False)
    checked_gather: orm.Mapped[Optional[bool]] = orm.mapped_column(default=False)
    checked_classify: orm.Mapped[Optional[bool]] = orm.mapped_column(default=False)
    checked_visualise: orm.Mapped[Optional[bool]] = orm.mapped_column(default=False)
    checked_explore: orm.Mapped[Optional[bool]] = orm.mapped_column(default=False)


class Project(ProjectBase, base_models.TimestampModel):
    """Project model that can inherit from multiple models."""

    __tablename__ = "projects"
    __table_args__ = (
        # Requests with `WHERE project_id and deleted_at is not null` will also use this index.
        Index("idx_project_id_deteted_at", "id", "deleted_at"),
        Index(
            "idx_deleted_at",
            "deleted_at",
        ),
    )

    # Relationship to get all related JobRuns for project, ordered by id descending
    job_runs = orm.relationship(
        "JobRuns",
        order_by="desc(JobRuns.id)",
        primaryjoin="Project.id == foreign(JobRuns.project_id)",
        lazy="dynamic",
    )

    @property
    def latest_job_run(self) -> job_run_models.JobRuns | None:
        """Property to get the most recent JobRun."""
        latest_run: job_run_models.JobRuns | None = self.job_runs.first()

        if latest_run is None:
            return None

        return latest_run

    @property
    def last_job_run_completed_at(self) -> datetime.datetime | None:
        """Property to get the last job run completed at."""
        last_complete_job_run: job_run_models.JobRuns | None = self.job_runs.filter(
            job_run_models.JobRuns.completed_at.isnot(None),
        ).first()
        if last_complete_job_run is None:
            return None

        return last_complete_job_run.completed_at
