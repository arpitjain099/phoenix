"""Instance runs model."""
import datetime
from typing import Optional

from phiphi import platform_db
from phiphi.api.instances.instance_runs import schemas
from sqlalchemy import ForeignKey, orm
from sqlalchemy.ext.hybrid import hybrid_property


class InstanceRuns(platform_db.Base):
    """Instance Runs Model."""

    __tablename__ = "instance_runs"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    instance_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("instances.id"))
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
        # Check if there are any running instance runs
        if self.failed_at:
            return schemas.RunStatus.failed
        elif self.completed_at:
            return schemas.RunStatus.completed
        elif self.started_processing_at:
            return schemas.RunStatus.processing
        else:
            return schemas.RunStatus.in_queue
