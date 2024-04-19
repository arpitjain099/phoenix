"""Project crud functionality."""
import sqlalchemy.orm

from phiphi.api import exceptions
from phiphi.api.environments import models as env_models
from phiphi.api.projects import models, schemas


def create_project(
    session: sqlalchemy.orm.Session, project: schemas.ProjectCreate
) -> schemas.ProjectResponse:
    """Create a new project."""
    db_environment = (
        session.query(env_models.Environment)
        .filter(env_models.Environment.slug == project.environment_slug)
        .first()
    )

    if db_environment is None:
        raise exceptions.EnvironmentNotFound()

    db_project = models.Project(**project.dict())
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return schemas.ProjectResponse.model_validate(db_project)


def update_project(
    session: sqlalchemy.orm.Session, project_id: int, project: schemas.ProjectUpdate
) -> schemas.ProjectResponse | None:
    """Update an project."""
    db_project = session.get(models.Project, project_id)
    if db_project is None:
        return None
    for field, value in project.dict(exclude_unset=True).items():
        setattr(db_project, field, value)
    session.commit()
    session.refresh(db_project)
    return schemas.ProjectResponse.model_validate(db_project)


def get_project(
    session: sqlalchemy.orm.Session, project_id: int
) -> schemas.ProjectResponse | None:
    """Get an project."""
    db_project = session.get(models.Project, project_id)
    if db_project is None:
        return None
    return schemas.ProjectResponse.model_validate(db_project)


def get_projects(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.ProjectResponse]:
    """Get projects."""
    query = sqlalchemy.select(models.Project).offset(start).limit(end)
    projects = session.scalars(query).all()
    if not projects:
        return []
    return [schemas.ProjectResponse.model_validate(project) for project in projects]


def get_db_project_with_guard(session: sqlalchemy.orm.Session, project_id: int) -> None:
    """Guard for null instnaces."""
    db_project = session.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise exceptions.ProjectNotFound()
