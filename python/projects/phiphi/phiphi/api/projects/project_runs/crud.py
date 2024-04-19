"""Project runs crud functionality."""

import sqlalchemy.orm
from phiphi.api import exceptions
from phiphi.api.projects import crud as project_crud
from phiphi.api.projects import models as project_models
from phiphi.api.projects.project_runs import models, schemas


def create_project_runs(
    session: sqlalchemy.orm.Session, project_id: int
) -> schemas.ProjectRunsResponse:
    """Create a new project run."""
    db_project = (
        session.query(project_models.Project)
        .filter(project_models.Project.id == project_id)
        .first()
    )

    if db_project is None:
        raise exceptions.ProjectNotFound()

    db_project_runs = models.ProjectRuns(
        environment_slug=db_project.environment_slug, project_id=project_id
    )

    session.add(db_project_runs)

    session.commit()
    session.refresh(db_project_runs)
    return schemas.ProjectRunsResponse.model_validate(db_project_runs)


def get_project_runs_by_run_status_filter(
    session: sqlalchemy.orm.Session,
    project_id: int,
    run_status: schemas.RunStatus | None,
    start: int = 0,
    end: int = 100,
) -> list[schemas.ProjectRunsResponse]:
    """Get all project runs."""
    project_crud.get_db_project_with_guard(session, project_id)

    query = session.query(models.ProjectRuns).filter(models.ProjectRuns.project_id == project_id)

    if run_status == schemas.RunStatus.failed:
        query = query.filter(models.ProjectRuns.failed_at.isnot(None))
    elif run_status == schemas.RunStatus.completed:
        query = query.filter(models.ProjectRuns.completed_at.isnot(None))
    elif run_status == schemas.RunStatus.processing:
        query = query.filter(models.ProjectRuns.started_processing_at.isnot(None))
    elif run_status == schemas.RunStatus.in_queue:
        query = query.filter(
            models.ProjectRuns.failed_at.is_(None),
            models.ProjectRuns.completed_at.is_(None),
            models.ProjectRuns.started_processing_at.is_(None),
        )
    elif run_status == schemas.RunStatus.yet_to_run:
        query = query.filter(
            models.ProjectRuns.failed_at.is_(None),
            models.ProjectRuns.completed_at.is_(None),
            models.ProjectRuns.started_processing_at.is_(None),
        )
    query = query.offset(start).limit(end)

    db_project_runs = session.scalars(query).all()

    if not db_project_runs:
        return []
    return [schemas.ProjectRunsResponse.model_validate(runs) for runs in db_project_runs]


def get_project_runs(
    session: sqlalchemy.orm.Session,
    project_id: int,
    start: int = 0,
    end: int = 100,
) -> list[schemas.ProjectRunsResponse]:
    """Get all project runs."""
    project_crud.get_db_project_with_guard(session, project_id)

    query = (
        sqlalchemy.select(models.ProjectRuns)
        .filter(models.ProjectRuns.project_id == project_id)
        .offset(start)
        .limit(end)
    )

    db_project_runs = session.scalars(query).all()

    if not db_project_runs:
        return []
    return [schemas.ProjectRunsResponse.model_validate(runs) for runs in db_project_runs]


def get_project_last_run(
    session: sqlalchemy.orm.Session, project_id: int
) -> schemas.ProjectRunsResponse | None:
    """Get last project run."""
    project_crud.get_db_project_with_guard(session, project_id)

    db_project_run = (
        session.query(models.ProjectRuns)
        .filter(models.ProjectRuns.project_id == project_id)
        .order_by(models.ProjectRuns.created_at.desc())
        .first()
    )

    if db_project_run is None:
        return None
    return schemas.ProjectRunsResponse.model_validate(db_project_run)


def update_project_runs(
    session: sqlalchemy.orm.Session, project_run_id: int, project_run: schemas.ProjectRunsUpdate
) -> schemas.ProjectRunsResponse | None:
    """Update an project run."""
    db_project_run = session.get(models.ProjectRuns, project_run_id)
    if db_project_run is None:
        return None
    for field, value in project_run.dict(exclude_unset=True).items():
        setattr(db_project_run, field, value)
    session.commit()
    session.refresh(db_project_run)
    return schemas.ProjectRunsResponse.model_validate(db_project_run)
