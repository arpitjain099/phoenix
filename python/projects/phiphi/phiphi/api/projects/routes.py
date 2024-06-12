"""Routes for the projects."""
import logging

import fastapi

from phiphi.api import deps
from phiphi.api.projects import crud, schemas

router = fastapi.APIRouter()

logger = logging.getLogger(__name__)


@router.post("/projects/", response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate, session: deps.SessionDep
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


@router.get("/projects/", response_model=list[schemas.ProjectResponse])
def get_projects(
    session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.ProjectResponse]:
    """Get Projects."""
    return crud.get_projects(session, start, end)


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, session: deps.SessionDep) -> None:
    """Delete an project."""
    crud.delete_project(session, project_id, delete_project_db=True)
    return None
