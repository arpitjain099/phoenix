"""Project Models."""
from typing import Optional, cast

from sqlalchemy import ForeignKey, orm
from sqlalchemy.ext.hybrid import hybrid_property

from phiphi import platform_db
from phiphi.api import base_models, base_schemas
from phiphi.api.projects.project_runs import models


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


class Project(ProjectBase, base_models.TimestampModel):
    """Project model that can inherit from multiple models."""

    __tablename__ = "projects"

    # Relationship to get all related ProjectRuns, ordered by created_at descending
    project_runs = orm.relationship(
        "ProjectRuns",
        order_by="desc(ProjectRuns.created_at)",
        primaryjoin="Project.id == ProjectRuns.project_id",
        lazy="dynamic",
    )

    @hybrid_property
    def last_run(self) -> models.ProjectRuns | None:
        """Property to get the most recent ProjectRun."""
        last_run = self.project_runs.first()

        if last_run is None:
            return None

        return cast(models.ProjectRuns, last_run)

    @hybrid_property
    def run_status(self) -> str:
        """Run status hybrid property."""
        # Check if there are any running project runs

        if self.last_run is None:
            return base_schemas.RunStatus.yet_to_run

        return self.last_run.run_status
