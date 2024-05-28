"""JobRun routes."""
from datetime import datetime
from typing import Any

import fastapi
from prefect.client.schemas import objects
from prefect.deployments import deployments
from sqlalchemy.orm import Session

from phiphi.api import deps
from phiphi.api.projects.job_runs import crud, schemas

router = fastapi.APIRouter()


async def wrapped_run_deployment(name: str, parameters: dict[str, Any]) -> objects.FlowRun:
    """Run a deployment.

    This has been wrapped otherwise we are unable to mock it.
    """
    flow_run: objects.FlowRun = await deployments.run_deployment(
        name=name,
        parameters=parameters,
        # Return the flow run immediately
        # and don't block
        timeout=0,
    )
    return flow_run


async def start_deployment(
    session: Session, name: str, job_run: schemas.JobRunResponse
) -> schemas.JobRunResponse:
    """Run a deployment."""
    parameters = {
        "project_id": job_run.project_id,
        "job_type": job_run.foreign_job_type,
        "job_source_id": job_run.foreign_id,
        "job_run_id": job_run.id,
    }
    # Can't use prefect.deployments.deployments here as we are not able to mock it in the tests
    flow_run = await wrapped_run_deployment(name=name, parameters=parameters)
    job_run_update_started = schemas.JobRunUpdateStarted(
        id=job_run.id, flow_run_id=str(flow_run.id), flow_run_name=flow_run.name
    )
    return crud.update_job_run(session, job_run_update_started)


@router.post("/projects/{project_id}/job_runs/", response_model=schemas.JobRunResponse)
async def create_job_run(
    project_id: int, session: deps.SessionDep, job_run_create: schemas.JobRunCreate
) -> schemas.JobRunResponse:
    """Create a Project Job Run.

    Args:
        project_id: ID of the project.
        job_run_create: Data to create the job run.
        deployment_name_prefix: Prefix to add to the deployment name.
        session: Database session.

    Returns:
        Created Job Run.
    """
    job_run = crud.create_job_run(session, project_id, job_run_create)
    try:
        job_run = await start_deployment(
            session=session, name="flow_runner_flow/flow_runner_flow", job_run=job_run
        )
    except Exception:
        job_run = crud.update_job_run(
            session,
            schemas.JobRunUpdateCompleted(
                id=job_run.id,
                status=schemas.Status.failed,
                completed_at=datetime.now(),
            ),
        )
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
    project_id: int, session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.JobRunResponse]:
    """Get Project Job Runs."""
    return crud.get_job_runs(session, project_id, start, end)
