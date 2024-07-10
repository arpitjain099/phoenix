"""JobRun routes."""
import logging
from datetime import datetime

import fastapi

from phiphi.api import deps
from phiphi.api.projects.job_runs import crud, prefect_deployment, schemas

router = fastapi.APIRouter()

logger = logging.getLogger(__name__)


@router.post("/projects/{project_id}/job_runs/", response_model=schemas.JobRunResponse)
async def create_job_run(
    project_id: int, session: deps.SessionDep, job_run_create: schemas.JobRunCreate
) -> schemas.JobRunResponse:
    """Create a Project Job Run.

    For tabulate types you must have a foreign_id of 0.

    Returns:
        Created Job Run.
    """
    job_run = crud.create_job_run(session, project_id, job_run_create)
    try:
        job_run = await prefect_deployment.start_deployment(
            session=session, name="flow_runner_flow/flow_runner_flow", job_run=job_run
        )
    except Exception as e:
        job_run = crud.update_job_run(
            session,
            schemas.JobRunUpdateCompleted(
                id=job_run.id,
                status=schemas.Status.failed,
                completed_at=datetime.now(),
            ),
        )
        logger.error("Error running deployment", exc_info=e)
    return job_run


@router.get("/projects/{project_id}/job_runs/{id}", response_model=schemas.JobRunResponse)
def get_job_run(project_id: int, id: int, session: deps.SessionDep) -> schemas.JobRunResponse:
    """Get a Project Job Run."""
    job_run = crud.get_job_run(session, project_id, id)
    if job_run is None:
        raise fastapi.HTTPException(status_code=404, detail="Job Run not found")
    return job_run


@router.get("/projects/{project_id}/job_runs/", response_model=list[schemas.JobRunResponse])
def get_job_runs(
    project_id: int,
    session: deps.SessionDep,
    start: int = 0,
    end: int = 100,
    foreign_job_type: schemas.ForeignJobType | None = None,
) -> list[schemas.JobRunResponse]:
    """Get Project Job Runs."""
    return crud.get_job_runs(session, project_id, start, end, foreign_job_type)
