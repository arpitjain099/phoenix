"""Job Run prefect deployment functionality."""
from typing import Any

from prefect.client.schemas import objects
from prefect.deployments import deployments
from sqlalchemy.orm import Session

from phiphi.api.projects.job_runs import crud, schemas


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
