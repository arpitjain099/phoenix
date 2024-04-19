"""Instance runs crud functionality."""

import sqlalchemy.orm
from phiphi.api import exceptions
from phiphi.api.instances import crud as instance_crud
from phiphi.api.instances import models as instance_models
from phiphi.api.instances.instance_runs import models, schemas


def create_instance_runs(
    session: sqlalchemy.orm.Session, instance_id: int
) -> schemas.InstanceRunsResponse:
    """Create a new instance run."""
    db_instance = (
        session.query(instance_models.Instance)
        .filter(instance_models.Instance.id == instance_id)
        .first()
    )

    if db_instance is None:
        raise exceptions.InstanceNotFound()

    db_instance_runs = models.InstanceRuns(
        environment_slug=db_instance.environment_slug, instance_id=instance_id
    )

    session.add(db_instance_runs)

    session.commit()
    session.refresh(db_instance_runs)
    return schemas.InstanceRunsResponse.model_validate(db_instance_runs)


def get_instance_runs_by_run_status_filter(
    session: sqlalchemy.orm.Session,
    instance_id: int,
    run_status: schemas.RunStatus | None,
    start: int = 0,
    end: int = 100,
) -> list[schemas.InstanceRunsResponse]:
    """Get all instance runs."""
    instance_crud.get_db_instance_with_guard(session, instance_id)

    query = session.query(models.InstanceRuns).filter(
        models.InstanceRuns.instance_id == instance_id
    )

    if run_status == schemas.RunStatus.failed:
        query = query.filter(models.InstanceRuns.failed_at.isnot(None))
    elif run_status == schemas.RunStatus.completed:
        query = query.filter(models.InstanceRuns.completed_at.isnot(None))
    elif run_status == schemas.RunStatus.processing:
        query = query.filter(models.InstanceRuns.started_processing_at.isnot(None))
    elif run_status == schemas.RunStatus.in_queue:
        query = query.filter(
            models.InstanceRuns.failed_at.is_(None),
            models.InstanceRuns.completed_at.is_(None),
            models.InstanceRuns.started_processing_at.is_(None),
        )
    elif run_status == schemas.RunStatus.yet_to_run:
        query = query.filter(
            models.InstanceRuns.failed_at.is_(None),
            models.InstanceRuns.completed_at.is_(None),
            models.InstanceRuns.started_processing_at.is_(None),
        )
    query = query.offset(start).limit(end)

    db_instance_runs = session.scalars(query).all()

    if not db_instance_runs:
        return []
    return [schemas.InstanceRunsResponse.model_validate(runs) for runs in db_instance_runs]


def get_instance_runs(
    session: sqlalchemy.orm.Session,
    instance_id: int,
    start: int = 0,
    end: int = 100,
) -> list[schemas.InstanceRunsResponse]:
    """Get all instance runs."""
    instance_crud.get_db_instance_with_guard(session, instance_id)

    query = (
        sqlalchemy.select(models.InstanceRuns)
        .filter(models.InstanceRuns.instance_id == instance_id)
        .offset(start)
        .limit(end)
    )

    db_instance_runs = session.scalars(query).all()

    if not db_instance_runs:
        return []
    return [schemas.InstanceRunsResponse.model_validate(runs) for runs in db_instance_runs]


def get_instance_last_run(
    session: sqlalchemy.orm.Session, instance_id: int
) -> schemas.InstanceRunsResponse | None:
    """Get last instance run."""
    instance_crud.get_db_instance_with_guard(session, instance_id)

    db_instance_run = (
        session.query(models.InstanceRuns)
        .filter(models.InstanceRuns.instance_id == instance_id)
        .order_by(models.InstanceRuns.created_at.desc())
        .first()
    )

    if db_instance_run is None:
        return None
    return schemas.InstanceRunsResponse.model_validate(db_instance_run)


def update_instance_runs(
    session: sqlalchemy.orm.Session, instance_run_id: int, instance_run: schemas.InstanceRunsUpdate
) -> schemas.InstanceRunsResponse | None:
    """Update an instance run."""
    db_instance_run = session.get(models.InstanceRuns, instance_run_id)
    if db_instance_run is None:
        return None
    for field, value in instance_run.dict(exclude_unset=True).items():
        setattr(db_instance_run, field, value)
    session.commit()
    session.refresh(db_instance_run)
    return schemas.InstanceRunsResponse.model_validate(db_instance_run)
