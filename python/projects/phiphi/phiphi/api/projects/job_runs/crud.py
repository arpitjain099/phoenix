"""Crud functionality for job runs."""
from typing import Union

from phiphi.api.projects.job_runs import models, schemas
from sqlalchemy.orm import Session


def create_job_run(
    db: Session, project_id: int, job_run_create: schemas.JobRunCreate
) -> schemas.JobRunResponse:
    """Create a new job run."""
    db_job_run = models.JobRuns(
        **job_run_create.dict(),
        status=schemas.Status.awaiting_start,
        project_id=project_id,
    )
    db.add(db_job_run)
    db.commit()
    db.refresh(db_job_run)
    return schemas.JobRunResponse.model_validate(db_job_run)


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


def get_job_run(db: Session, project_id: int, job_run_id: int) -> schemas.JobRunResponse | None:
    """Get a job run."""
    db_job_run = (
        db.query(models.JobRuns)
        .filter(models.JobRuns.project_id == project_id, models.JobRuns.id == job_run_id)
        .first()
    )
    if db_job_run is None:
        return None
    return schemas.JobRunResponse.model_validate(db_job_run)


def get_job_runs(
    db: Session, project_id: int, start: int = 0, end: int = 100
) -> list[schemas.JobRunResponse]:
    """Get job runs."""
    db_job_runs = (
        db.query(models.JobRuns)
        .filter(models.JobRuns.project_id == project_id)
        .order_by(models.JobRuns.id.desc())
        .slice(start, end)
        .all()
    )
    return [schemas.JobRunResponse.model_validate(db_job_run) for db_job_run in db_job_runs]
