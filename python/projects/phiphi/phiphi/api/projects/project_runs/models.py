"""Project runs model."""
import datetime
from typing import Optional

from phiphi import platform_db
from phiphi.api import base_schemas
from sqlalchemy import ForeignKey, orm
from sqlalchemy.ext.hybrid import hybrid_property


class ProjectRuns(platform_db.Base):
    """Project Runs Model."""

    __tablename__ = "project_runs"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    project_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("projects.id"))
    started_processing_at: orm.Mapped[Optional[datetime.datetime]]
    environment_slug: orm.Mapped[str]
    completed_at: orm.Mapped[Optional[datetime.datetime]]
    failed_at: orm.Mapped[Optional[datetime.datetime]]
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        default=lambda: datetime.datetime.now()
    )

    @hybrid_property
    def run_status(self) -> str:
        """Run status hybrid property."""
        # Check if there are any running project runs
        if self.failed_at:
            return base_schemas.RunStatus.failed
        elif self.completed_at:
            return base_schemas.RunStatus.completed
        elif self.started_processing_at:
            return base_schemas.RunStatus.processing
        else:
            return base_schemas.RunStatus.in_queue
