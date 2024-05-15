"""Routes for gathers."""
import fastapi
from phiphi.api import base_schemas, deps
from phiphi.api.projects.project_runs import crud, schemas

router = fastapi.APIRouter()


@router.post("/projects/{project_id}/runs/", response_model=schemas.ProjectRunsResponse)
def create_project_runs(
    project_id: int,
    session: deps.SessionDep,
) -> schemas.ProjectRunsResponse:
    """Create a new project run."""
    return crud.create_project_runs(session, project_id)


@router.get("/projects/{project_id}/runs/", response_model=list[schemas.ProjectRunsResponse])
def get_project_runs(
    session: deps.SessionDep,
    project_id: int,
    run_status: base_schemas.RunStatus | None = None,
    start: int = 0,
    end: int = 100,
) -> list[schemas.ProjectRunsResponse]:
    """Get project runs."""
    if run_status is None:
        return crud.get_project_runs(session, project_id, start, end)
    else:
        return crud.get_project_runs_by_run_status_filter(
            session, project_id, run_status, start, end
        )


@router.get(
    "/projects/{project_id}/runs/last/",
    response_model=schemas.ProjectRunsResponse,
)
def get_project_last_run(project_id: int, session: deps.SessionDep) -> schemas.ProjectRunsResponse:
    """Get last project run."""
    project_runs = crud.get_project_last_run(session, project_id)
    if project_runs is None:
        raise fastapi.HTTPException(status_code=404, detail="Project has no previous runs")
    return project_runs
