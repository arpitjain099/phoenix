"""Job runs models.

Implementation notes:
    - It may be possible that we can get real foreign key constraints by using the parent-child
      table pattern, and have one child tables per job type.
"""
import datetime
from typing import Optional

from phiphi import platform_db
from sqlalchemy import orm


class JobRuns(platform_db.Base):
    """Job runs model."""

    __tablename__ = "job_runs"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    row_created_at: orm.Mapped[datetime.datetime]
    foreign_id: orm.Mapped[int]
    foreign_job_type: orm.Mapped[str]
    status: orm.Mapped[Optional[str]]
    flow_run_id: orm.Mapped[Optional[str]]
    # Note: name of the _flow run_, not the flow. Useful for searching in Prefect UI.
    flow_run_name: orm.Mapped[Optional[str]]
    started_processing_at: orm.Mapped[Optional[datetime.datetime]]
    completed_at: orm.Mapped[Optional[datetime.datetime]]
