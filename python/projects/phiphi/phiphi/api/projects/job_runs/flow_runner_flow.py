"""Module containing (outer) flow which runs jobs (inner flows) and records their status."""
import asyncio
from typing import Coroutine, Union

from prefect import flow, task
from prefect.client.schemas import objects
from prefect.deployments import deployments
from prefect.flow_runs import wait_for_flow_run

from phiphi import constants, platform_db
from phiphi.api.projects import gathers, job_runs
from phiphi.pipeline_jobs.gathers import apify_input_schemas
from phiphi.types import PhiphiJobType


@task
def read_job_params(
    project_id: int, job_type: PhiphiJobType, job_source_id: int
) -> Union[apify_input_schemas.ApifyFacebookPostsInput]:
    """Task to read the job's params from the database.

    Args:
        project_id: ID of the project.
        job_type: Type of job to run.
        job_source_id: ID of the source for the job. I.e., if type is `gather` then
            `job_source_id` is the ID of the row in the gathers table.
    """
    if job_type == "gather":
        with platform_db.get_session_context() as session:
            gather = gathers.crud.get_gather(
                session=session, project_id=project_id, gather_id=job_source_id
            )
        if gather is None:
            raise ValueError(f"Gather with ID {job_source_id=} not found.")
        elif type(gather) == gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse:
            job_params = apify_input_schemas.ApifyFacebookPostsInput(
                only_posts_older_than=gather.only_posts_older_than,
                only_posts_newer_than=gather.only_posts_newer_than,
                account_urls=gather.account_url_list,
                results_per_url_limit=gather.limit_posts_per_account,
            )
        else:
            raise NotImplementedError(f"Run for gather type {type(gather)=} not implemented yet.")
    else:
        raise NotImplementedError(f"Job type {job_type=} not implemented yet.")

    return job_params


@task
def start_flow_run(
    project_id: int,
    job_type: PhiphiJobType,
    job_source_id: int,
    job_run_id: int,
    job_params: Union[apify_input_schemas.ApifyFacebookPostsInput],
) -> objects.FlowRun:
    """Start the (inner) flow for the job.

    Args:
        project_id: ID of the project.
        job_type: Type of job to run.
        job_source_id: ID of the source for the job. Corresponds to the job_type table.
        job_run_id: ID of the row in the job_runs table.
        job_params: Parameters for the job.
    """
    if type(job_params) == apify_input_schemas.ApifyFacebookPostsInput:
        deployment_name = "gather_apify_facebook_posts_flow/main_deployment"
    else:
        raise NotImplementedError(
            f"Run for job_params type {type(job_params)=} not implemented yet."
        )
    job_run_flow: objects.FlowRun = asyncio.run(
        deployments.run_deployment(
            name=deployment_name,
            parameters=job_params.dict(by_alias=True),
            as_subflow=True,
            timeout=0,  # this means it returns immediately with the metadata
            tags=[
                f"project_id:{project_id}",
                f"job_type:{job_type}",
                f"job_source_id:{job_source_id}",
                f"job_run_id:{job_run_id}",
            ],
        )
    )
    return job_run_flow


@task
def job_run_update_started(job_run_id: int) -> None:
    """Update the job_runs row with this (outer) flow's info and set job row status to started.

    Args:
        job_run_id: ID of the row in the job_runs table.
    """
    job_run_update_processing = job_runs.schemas.JobRunUpdateProcessing(
        id=job_run_id,
    )
    with platform_db.get_session_context() as session:
        job_runs.crud.update_job_run(db=session, job_run_data=job_run_update_processing)


@task
def wait_for_job_flow_run(job_run_flow: objects.FlowRun) -> objects.FlowRun:
    """Wait for the inner flow to complete and fetch the final state."""
    flow_run_result: objects.FlowRun = asyncio.run(wait_for_flow_run(flow_run_id=job_run_flow.id))
    return flow_run_result


@task
def job_run_update_completed(job_run_id: int, job_run_flow_result: objects.FlowRun) -> None:
    """Update the job_runs table with the final state of the job (the inner flow)."""
    assert job_run_flow_result.state is not None
    status = (
        job_runs.schemas.Status.completed_sucessfully
        if job_run_flow_result.state.is_completed()
        else job_runs.schemas.Status.failed
    )

    job_run_update_completed = job_runs.schemas.JobRunUpdateCompleted(id=job_run_id, status=status)
    with platform_db.get_session_context() as session:
        job_runs.crud.update_job_run(db=session, job_run_data=job_run_update_completed)


@flow(name="flow_runner_flow")
def flow_runner_flow(
    project_id: int,
    job_type: PhiphiJobType,
    job_source_id: int,
    job_run_id: int,
) -> None:
    """Flow which runs flow deployments and records their status.

    Args:
        project_id: ID of the project.
        job_type: Type of job to run.
        job_source_id: ID of the source for the job. I.e., if type is `gather` then
            `job_source_id` is the ID of the row in the gathers table.
        job_run_id: ID of the row in the job_runs table.
    """
    job_params = read_job_params(
        project_id=project_id, job_type=job_type, job_source_id=job_source_id
    )
    job_run_flow = start_flow_run(
        project_id=project_id,
        job_type=job_type,
        job_source_id=job_source_id,
        job_run_id=job_run_id,
        job_params=job_params,
    )
    job_run_update_started(job_run_id=job_run_id)
    job_run_flow_result = wait_for_job_flow_run(job_run_flow=job_run_flow)
    job_run_update_completed(job_run_id=job_run_id, job_run_flow_result=job_run_flow_result)


def create_deployments(
    override_work_pool_name: str | None = None,
    deployment_name_prefix: str = "",
    image: str = constants.DEFAULT_IMAGE,
    tags: list[str] = [],
    build: bool = False,
    push: bool = False,
) -> list[Coroutine]:
    """Create deployments for flow_runner_flow.

    Args:
        override_work_pool_name (str | None): The name of the work pool to use to override the
        default work pool.
        deployment_name_prefix (str, optional): The prefix of the deployment name. Defaults to "".
        image (str, optional): The image to use for the deployments. Defaults to
        constants.DEFAULT_IMAGE.
        tags (list[str], optional): The tags to use for the deployments. Defaults to [].
        build (bool, optional): If True, build the image. Defaults to False.
        push (bool, optional): If True, push the image. Defaults to False.

    Returns:
        list[Coroutine]: List of coroutines that create deployments.
    """
    work_pool_name = str(constants.WorkPool.main)
    if override_work_pool_name:
        work_pool_name = override_work_pool_name
    task = flow_runner_flow.deploy(
        name=deployment_name_prefix + "flow_runner_flow",
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
