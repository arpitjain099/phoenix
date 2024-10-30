"""Routes for the projects."""
import logging

import fastapi

from phiphi.api import deps
from phiphi.api.projects import crud, schemas, user_project_associations

router = fastapi.APIRouter()

logger = logging.getLogger(__name__)


@router.post("/projects/", response_model=schemas.ProjectResponse)
def create_project(
    admin_user: deps.AdminOnlyUser, project: schemas.ProjectCreate, session: deps.SessionDep
) -> schemas.ProjectResponse:
    """Create a new project."""
    try:
        project_response = crud.create_project(session, project, init_project_db=True)
        return project_response
    # fastapi.HTTPException have their own status code and detail
    except fastapi.HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Project creation failed: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Project creation failed")


@router.put("/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int, project: schemas.ProjectUpdate, session: deps.SessionDep
) -> schemas.ProjectResponse:
    """Update an project."""
    updated_project = crud.update_project(session, project_id, project)
    if updated_project is None:
        raise fastapi.HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, session: deps.SessionDep) -> schemas.ProjectResponse:
    """Get an Project."""
    project = crud.get_project(session, project_id)
    if project is None:
        raise fastapi.HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/projects/", response_model=list[schemas.ProjectListResponse])
def get_projects(
    session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.ProjectListResponse]:
    """Get Projects."""
    return crud.get_projects(session, start, end)


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, session: deps.SessionDep) -> None:
    """Delete an project."""
    try:
        crud.delete_project(session, project_id, delete_project_db=True)
        return None
    except fastapi.HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Project deletion failed: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Project deletion failed")


@router.post("/projects/{project_id}/users/{user_id}")
def add_user_to_project(
    admin_user: deps.AdminOnlyUser,
    project_id: int,
    user_id: int,
    create_obj: user_project_associations.UserProjectAssociationCreate,
    session: deps.SessionDep,
) -> user_project_associations.UserProjectAssociationResponse:
    """Add a user to a project."""
    return user_project_associations.create_user_project_association(
        session, project_id, user_id, create_obj
    )


@router.delete("/projects/{project_id}/users/{user_id}")
def remove_user_from_project(
    admin_user: deps.AdminOnlyUser, project_id: int, user_id: int, session: deps.SessionDep
) -> None:
    """Remove a user from a project."""
    user_project_associations.delete_user_project_association(session, project_id, user_id)
    return None
