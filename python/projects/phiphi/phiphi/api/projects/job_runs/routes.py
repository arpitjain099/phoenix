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
