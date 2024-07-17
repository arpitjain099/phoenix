"""Crud functionality for job runs."""
import logging
from datetime import datetime
from typing import Union

from sqlalchemy.orm import Session

from phiphi.api import exceptions
from phiphi.api.projects.job_runs import models, prefect_deployment, schemas

logger = logging.getLogger(__name__)


def check_valid_gather(db: Session, project_id: int, gather_id: int) -> bool:
    """Check if the gather exists and is valid.

    If the gather is not found or is invalid, raise an exception.
    """
    from phiphi.api.projects.gathers import crud as gather_crud

    gather = gather_crud.get_gather(db, project_id, gather_id)
    if gather is None:
        raise exceptions.GatherNotFound()

    return True


def invalid_foreign_object_guard(
    db: Session, project_id: int, foreign_id: int, foreign_job_type: schemas.ForeignJobType
) -> None:
    """Guard to check if the foreign object exists."""
    if foreign_job_type == schemas.ForeignJobType.gather:
        check_valid_gather(db, project_id, foreign_id)

    if foreign_job_type == schemas.ForeignJobType.tabulate and foreign_id != 0:
        raise exceptions.HttpException400("Tabulate must have a foreign_id of 0")

    latest_job_run = get_latest_job_run(db, project_id, foreign_id, foreign_job_type)
    if latest_job_run and not latest_job_run.completed_at:
        raise exceptions.ForeignObjectHasActiveJobRun(foreign_id, str(foreign_job_type))


def create_job_run(
    db: Session, project_id: int, job_run_create: schemas.JobRunCreate
) -> schemas.JobRunResponse:
    """Create a new job run."""
    invalid_foreign_object_guard(
        db, project_id, job_run_create.foreign_id, job_run_create.foreign_job_type
    )
    orm_job_run = models.JobRuns(
        **job_run_create.dict(),
        status=schemas.Status.awaiting_start,
        project_id=project_id,
    )
    db.add(orm_job_run)
    db.commit()
    db.refresh(orm_job_run)
    return schemas.JobRunResponse.model_validate(orm_job_run)


def update_job_run(
    db: Session,
    job_run_data: Union[
        schemas.JobRunUpdateStarted, schemas.JobRunUpdateCompleted, schemas.JobRunUpdateProcessing
    ],
) -> schemas.JobRunResponse:
    """Update a job run.

    Note that only the schemas giving in the signature are allowed to be passed in.
    """
    orm_job_run = db.query(models.JobRuns).filter(models.JobRuns.id == job_run_data.id).first()
    if orm_job_run:
        for field, value in job_run_data.dict(exclude={"id"}).items():
            setattr(orm_job_run, field, value)
        db.commit()

    return schemas.JobRunResponse.model_validate(orm_job_run)


def get_job_run(db: Session, project_id: int, job_run_id: int) -> schemas.JobRunResponse | None:
    """Get a job run."""
    orm_job_run = (
        db.query(models.JobRuns)
        .filter(models.JobRuns.project_id == project_id, models.JobRuns.id == job_run_id)
        .first()
    )
    if orm_job_run is None:
        return None
    return schemas.JobRunResponse.model_validate(orm_job_run)


def get_job_runs(
    db: Session,
    project_id: int,
    start: int = 0,
    end: int = 100,
    foreign_job_type: schemas.ForeignJobType | None = None,
) -> list[schemas.JobRunResponse]:
    """Get job runs."""
    query = db.query(models.JobRuns).filter(models.JobRuns.project_id == project_id)
    if foreign_job_type:
        query = query.filter(models.JobRuns.foreign_job_type == foreign_job_type)
    orm_job_runs = query.order_by(models.JobRuns.id.desc()).slice(start, end).all()
    return [schemas.JobRunResponse.model_validate(orm_job_run) for orm_job_run in orm_job_runs]


def get_latest_job_run(
    db: Session,
    project_id: int,
    foreign_id: int | None = None,
    foreign_job_type: schemas.ForeignJobType | None = None,
) -> schemas.JobRunResponse | None:
    """Get the latest job run."""
    query = db.query(models.JobRuns).filter(models.JobRuns.project_id == project_id)
    if foreign_id:
        query = query.filter(models.JobRuns.foreign_id == foreign_id)
    if foreign_job_type:
        query = query.filter(models.JobRuns.foreign_job_type == foreign_job_type)
    orm_job_run = query.order_by(models.JobRuns.id.desc()).first()
    if orm_job_run is None:
        return None
    return schemas.JobRunResponse.model_validate(orm_job_run)


async def create_and_run_job_run(
    db: Session, project_id: int, job_run_create: schemas.JobRunCreate
) -> schemas.JobRunResponse:
    """Create a new job run and run it."""
    job_run = create_job_run(db, project_id, job_run_create)
    try:
        job_run = await prefect_deployment.start_deployment(
            session=db, name="flow_runner_flow/flow_runner_flow", job_run=job_run
        )
    except Exception as e:
        job_run = update_job_run(
            db,
            schemas.JobRunUpdateCompleted(
                id=job_run.id,
                status=schemas.Status.failed,
                completed_at=datetime.now(),
            ),
        )
        logger.error("Error running deployment", exc_info=e)
    return job_run
