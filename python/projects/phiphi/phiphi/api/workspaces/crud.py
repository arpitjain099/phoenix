"""Workspace crud functionality."""
import slugify
import sqlalchemy.orm
from phiphi.api import utility
from phiphi.api.workspaces import models, schemas


def create_workspace(
    session: sqlalchemy.orm.Session, workspace: schemas.WorkspaceCreate
) -> schemas.WorkspaceResponse:
    """Create a new workspace."""
    slug_exist = (
        session.query(models.Workspace).filter(models.Workspace.slug == workspace.slug).first()
    )

    if slug_exist:
        raise Exception("Slug already exists")

    workspace.name = slugify.slugify(workspace.name)
    db_workspace = models.Workspace(**workspace.dict())
    session.add(db_workspace)
    session.commit()
    session.refresh(db_workspace)
    return schemas.WorkspaceResponse.model_validate(db_workspace)


def get_workspace(session: sqlalchemy.orm.Session, slug: str) -> schemas.WorkspaceResponse | None:
    """Get an workspace."""
    db_workspace = session.query(models.Workspace).filter(models.Workspace.slug == slug).first()

    if db_workspace is None:
        return None
    return schemas.WorkspaceResponse.model_validate(db_workspace)


def get_workspace_by_slug(
    session: sqlalchemy.orm.Session, slug: str
) -> schemas.WorkspaceResponse | None:
    """Get an workspace."""
    db_workspace = session.query(models.Workspace).filter(models.Workspace.slug == slug).first()
    if db_workspace is None:
        return None
    return schemas.WorkspaceResponse.model_validate(db_workspace)


def get_workspaces(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.WorkspaceResponse]:
    """Get workspaces."""
    query = sqlalchemy.select(models.Workspace).offset(start).limit(end)
    workspaces = session.scalars(query).all()
    if not workspaces:
        return []
    return [schemas.WorkspaceResponse.model_validate(workspace) for workspace in workspaces]


def update_workspace(
    session: sqlalchemy.orm.Session, workspace_id: int, workspace: schemas.WorkspaceUpdate
) -> schemas.WorkspaceResponse | None:
    """Update an workspace."""
    db_workspace = session.get(models.Workspace, workspace_id)
    if db_workspace is None:
        return None
    for field, value in workspace.dict(exclude_unset=True).items():
        setattr(db_workspace, field, value)
    session.commit()
    session.refresh(db_workspace)
    return schemas.WorkspaceResponse.model_validate(db_workspace)


def get_unique_slug(session: sqlalchemy.orm.Session, workspace_name: str) -> schemas.SlugResponse:
    """Get unique slug."""
    # validation for empty string
    if not workspace_name.strip():
        raise Exception("Please enter a valid string")

    slug_exist = (
        session.query(models.Workspace).filter(models.Workspace.slug == workspace_name).first()
    )

    name = slugify.slugify(workspace_name)

    if slug_exist:
        random_str = utility.generate_random_string(4)
        slug = "{}-{}".format(name, random_str)

    else:
        slug = name

    response = schemas.SlugResponse(slug=slug)

    return schemas.SlugResponse.model_validate(response)
