"""Project crud functionality."""
import datetime

import sqlalchemy.orm

from phiphi import config, utils
from phiphi.api import exceptions
from phiphi.api.projects import models, schemas
from phiphi.api.workspaces import models as workspace_models
from phiphi.pipeline_jobs import projects


def create_project(
    session: sqlalchemy.orm.Session, project: schemas.ProjectCreate, init_project_db: bool = False
) -> schemas.ProjectResponse:
    """Create a new project."""
    orm_workspace = (
        session.query(workspace_models.Workspace)
        .filter(workspace_models.Workspace.slug == project.workspace_slug)
        .first()
    )

    if orm_workspace is None:
        raise exceptions.WorkspaceNotFound()

    try:
        orm_project = models.Project(**project.dict())
        session.add(orm_project)
        # Get the id of the project without commiting the transaction
        session.flush()
        if init_project_db and not config.settings.USE_MOCK_BQ:
            project_namespace = utils.get_project_namespace(orm_project.id)
            # Creating with dummy rows as it is easy to test the dashboard
            projects.init_project_db(
                project_namespace, orm_project.workspace_slug, with_dummy_data=True
            )
        session.commit()
        session.refresh(orm_project)
        return schemas.ProjectResponse.model_validate(orm_project)
    except Exception as e:
        session.rollback()  # Rollback the transaction if any error occurs
        raise e


def update_project(
    session: sqlalchemy.orm.Session, project_id: int, project: schemas.ProjectUpdate
) -> schemas.ProjectResponse | None:
    """Update an project."""
    orm_project = get_non_deleted_project_model(session, project_id)
    if orm_project is None:
        return None
    for field, value in project.dict(exclude_unset=True).items():
        setattr(orm_project, field, value)
    session.commit()
    session.refresh(orm_project)
    return schemas.ProjectResponse.model_validate(orm_project)


def get_project(
    session: sqlalchemy.orm.Session, project_id: int
) -> schemas.ProjectResponse | None:
    """Get an project."""
    orm_project = get_non_deleted_project_model(session, project_id)
    if orm_project is None:
        return None
    return schemas.ProjectResponse.model_validate(orm_project)


def get_all_projects(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.ProjectListResponse]:
    """Get projects."""
    query = (
        sqlalchemy.select(models.Project)
        .filter(models.Project.deleted_at.is_(None))
        .order_by(models.Project.id.desc())
        .offset(start)
        .limit(end)
    )
    projects = session.scalars(query).all()
    if not projects:
        return []
    return [schemas.ProjectListResponse.model_validate(project) for project in projects]


def get_user_projects(
    session: sqlalchemy.orm.Session, user_id: int, start: int = 0, end: int = 100
) -> list[schemas.ProjectListResponse]:
    """Get projects for a user."""
    # To be implemented
    pass


def get_orm_project_with_guard(session: sqlalchemy.orm.Session, project_id: int) -> None:
    """Guard for null instnaces."""
    orm_project = get_non_deleted_project_model(session, project_id)
    if orm_project is None:
        raise exceptions.ProjectNotFound()


def get_non_deleted_project_model(
    session: sqlalchemy.orm.Session, project_id: int
) -> models.Project | None:
    """Get a non-deleted project model."""
    orm_project = (
        session.query(models.Project)
        .filter(
            models.Project.deleted_at.is_(None),
            models.Project.id == project_id,
        )
        .first()
    )
    return orm_project


def delete_project(
    session: sqlalchemy.orm.Session, project_id: int, delete_project_db: bool = False
) -> None:
    """Delete an project."""
    orm_project = get_non_deleted_project_model(session, project_id)
    if orm_project is None:
        raise exceptions.ProjectNotFound()
    if delete_project_db and not config.settings.USE_MOCK_BQ:
        project_namespace = utils.get_project_namespace(project_id)
        projects.delete_project_db(project_namespace)
    orm_project.deleted_at = datetime.datetime.utcnow()
    session.add(orm_project)
    session.commit()
    return None
