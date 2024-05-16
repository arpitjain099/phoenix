"""Crud functionality for job runs."""
from typing import Union

from phiphi.api.projects.job_runs import models, schemas
from sqlalchemy.orm import Session


def create_job_run(db: Session, job_run_data: schemas.JobRunCreate) -> int:
    """Create a new job run."""
    db_job_run = models.JobRuns(**job_run_data.dict(), status=schemas.Status.awaiting_start)
    db.add(db_job_run)
    db.commit()
    db.refresh(db_job_run)
    return db_job_run.id


def update_job_run(
    db: Session, job_run_data: Union[schemas.JobRunUpdateStarted, schemas.JobRunUpdateCompleted]
) -> None:
    """Update a job run.

    Note that only the schemas giving in the signature are allowed to be passed in.
    """
    db_job_run = db.query(models.JobRuns).filter(models.JobRuns.id == job_run_data.id).first()
    if db_job_run:
        for field, value in job_run_data.dict(exclude={"id"}).items():
            setattr(db_job_run, field, value)
        db.commit()
