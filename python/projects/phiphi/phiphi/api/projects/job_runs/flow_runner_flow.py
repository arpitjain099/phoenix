"""Module containing (outer) flow which runs jobs (inner flows) and records their status.

NOTE: Much of this functionality is stub/placeholder code.

Depends on:
- gathers and its child tables; to pull gather params and parse to pass for inner flow
- inner flows (i.e. gather_apify_facebook_posts_flow and its params)
- job_runs table; to create job_runs and update their status

Likely this will become a module with sub-modules.
"""
import asyncio
from datetime import datetime
from typing import Any

from phiphi.types import PhiphiJobType
from prefect import flow, runtime, task
from prefect.client.schemas import objects
from prefect.deployments import deployments
from prefect.flow_runs import wait_for_flow_run


@task
def read_job_params(job_type: PhiphiJobType, job_source_id: int) -> dict:
    """Task to read job params from the database.

    Args:
        job_type: Type of job to run.
        job_source_id: ID of the source for the job. I.e., if type is `gather` then
            `job_source_id` is the ID of the row in the gathers table.

    Returns:
        job_params_dict: Job parameters.
    """
    job_params_dict: dict
    # Read job params from the database
    if job_type == "gather":
        # Read row with id from gathers table
        job_params_dict = {}
    elif job_type == "classify":
        # Read row with id from classifies table
        job_params_dict = {}
    elif job_type == "tabulate":
        # Read row with id from tabulates table
        job_params_dict = {}

    return job_params_dict


@task
def create_job_run_row(job_type: PhiphiJobType, job_source_id: int) -> int:
    """Task to create a row in the job_runs table.

    Returns:
        job_run_id: ID of the created row.
    """
    _ = {
        "foreign_id": job_source_id,
        "foreign_type": job_type,
        "prefect_outer_flow_run_id": runtime.flow_run.id,
        "prefect_outer_flow_run_name": runtime.flow_run.name,
    }
    # Create row in job_runs table
    # Get id of the created row
    return 1  # id of the created row


@task
def start_flow_run(job_type: PhiphiJobType, job_params: dict) -> objects.FlowRun:
    """Task to start the (inner) flow for the job.

    Args:
        job_type: Type of job to run.
        job_params: Parameters for the job.
    """
    # if job_type == "gather":  # and other if statements for other job types
    # TODO: we could add `tags` to tag with the project name/ID?
    job_run_flow: objects.FlowRun = asyncio.run(
        deployments.run_deployment(
            name="gather_apify_facebook_posts_flow/main_deployment",
            parameters=job_params,
            as_subflow=True,
            timeout=0,  # this means it returns immediately with the metadata
        )
    )
    return job_run_flow


@task
def update_job_row_to_started(job_run_id: int, job_run_flow: objects.FlowRun) -> None:
    """Update the job_runs table with info about the job and set status to started.

    Args:
        job_run_id: ID of the row in the job_runs table.
        job_run_flow: Flow run object for the job.
    """
    _ = {
        "prefect_inner_flow_run_id": job_run_flow.id,
        "prefect_inner_flow_run_name": job_run_flow.name,
        "prefect_inner_flow_run_status": "started",
        "prefect_inner_flow_run_started_at": datetime.now(),
    }
    # Update row in job_runs table for `job_run_id`


@task
def wait_for_job_flow_run(job_run_flow: objects.FlowRun) -> objects.FlowRun:
    """Wait for the inner flow to complete and fetch the final state."""
    flow_run_result: objects.FlowRun = asyncio.run(wait_for_flow_run(flow_run_id=job_run_flow.id))
    return flow_run_result


@task
def update_job_row_with_end_result(job_run_id: int, job_run_flow_result: objects.FlowRun) -> None:
    """Update the job_runs table with the final state of the job."""
    d: dict[str, Any] = {
        "prefect_inner_flow_run_status": job_run_flow_result.state,
    }
    if job_run_flow_result.state == "Success":
        d["prefect_inner_flow_run_completed_at"] = datetime.now()
    # Update row in job_runs table for `job_run_id`


@flow(name="flow_runner_flow")
def flow_runner_flow(job_type: PhiphiJobType, job_source_id: int) -> None:
    """Flow which runs flow deployments and records their status.

    Args:
        job_type: Type of job to run.
        job_source_id: ID of the source for the job. I.e., if type is `gather` then
            `job_source_id` is the ID of the row in the gathers table.
    """
    job_params = read_job_params(job_type=job_type, job_source_id=job_source_id)
    job_run_id = create_job_run_row(job_type=job_type, job_source_id=job_source_id)
    job_run_flow = start_flow_run(job_type=job_type, job_params=job_params)
    update_job_row_to_started(job_run_id=job_run_id, job_run_flow=job_run_flow)
    job_run_flow_result = wait_for_job_flow_run(job_run_flow=job_run_flow)
    update_job_row_with_end_result(job_run_id=job_run_id, job_run_flow_result=job_run_flow_result)


if __name__ == "__main__":
    asyncio.run(
        flow_runner_flow.deploy(
            name="main_deployment",
            work_pool_name="TODO",  # this should be the work pool on k8s ye?
            image="TODO",  # this should be the phiphi image!
            tags=["TODO"],
            build=False,
        )
    )
