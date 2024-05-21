"""JobRun routes."""
import fastapi
from phiphi.api import deps
from phiphi.api.projects.job_runs import crud, schemas

router = fastapi.APIRouter()


@router.post("/projects/{project_id}/job_runs/", response_model=schemas.JobRunResponse)
def create_job_run(
    project_id: int, session: deps.SessionDep, job_run_create: schemas.JobRunCreate
) -> schemas.JobRunResponse:
    """Create a Project Job Run."""
    return crud.create_job_run(session, project_id, job_run_create)


@router.get("/projects/{project_id}/job_runs/{id}", response_model=schemas.JobRunResponse)
def get_job_run(project_id: int, id: int, session: deps.SessionDep) -> schemas.JobRunResponse:
    """Get a Project Job Run."""
    job_run = crud.get_job_run(session, project_id, id)
    if job_run is None:
        raise fastapi.HTTPException(status_code=404, detail="Job Run not found")
    return job_run


@router.get("/projects/{project_id}/job_runs/", response_model=list[schemas.JobRunResponse])
def get_job_runs(
    project_id: int, session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.JobRunResponse]:
    """Get Project Job Runs."""
    return crud.get_job_runs(session, project_id, start, end)
