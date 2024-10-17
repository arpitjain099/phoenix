"""Module containing (outer) flow which runs jobs (inner flows) and records their status."""
import uuid
from typing import Any, Coroutine

import prefect
from prefect import flow, flow_runs, task
from prefect.client.schemas import objects
from prefect.deployments import deployments

from phiphi import (
    # Need to import the Base for the polymorphic_identity to work
    all_platform_models,  # noqa: F401
    constants,
    platform_db,
    utils,
)
from phiphi.api.projects import classifiers, gathers, job_runs
from phiphi.api.projects.job_runs import schemas


def get_gather_flow_params(project_id: int, gather_id: int) -> dict[str, Any]:
    """Get the parameters for the gather flow."""
    with platform_db.get_session_context() as session:
        gather = gathers.child_crud.get_child_gather(
            session=session, project_id=project_id, gather_id=gather_id
        )
    if gather is None:
        raise ValueError(f"Gather with {project_id=}, {gather_id=} not found.")
    params = {
        "gather_dict": gather.model_dump(),
        "gather_child_type": gather.child_type.value,
    }
    return params


def get_classify_flow_params(project_id: int, classifier_id: int) -> dict[str, Any]:
    """Get the parameters for the classify flow."""
    with platform_db.get_session_context() as session:
        classifier = classifiers.crud_v2.get_pipeline_classifier(
            session=session, project_id=project_id, classifier_id=classifier_id
        )
    if classifier is None:
        raise ValueError(
            f"Classifier with {project_id=}, {classifier_id=} not found, "
            " or is not a valid pipeline classifier."
        )
    params = {
        "classifier_dict": classifier.model_dump(),
    }
    return params


def get_all_classifiers_params(project_id: int) -> dict[str, Any]:
    """Get list of specs for all classifiers."""
    with platform_db.get_session_context() as session:
        classifiers_list = classifiers.crud_v2.get_pipeline_classifiers(
            session=session, project_id=project_id
        )
    params = {
        "classifiers_dict_list": [_classifier.model_dump() for _classifier in classifiers_list],
    }
    return params


def get_tabulate_flow_params(project_id: int) -> dict[str, Any]:
    """Get the parameters for the tabulate flow.

    Tabulate needs to know which classifiers are still active in the project, and what their latest
    version is, so that it can pull the correct classification data.
    """
    with platform_db.get_session_context() as session:
        classifiers_list = classifiers.crud_v2.get_pipeline_classifiers(
            session=session, project_id=project_id
        )
    params = {
        "active_classifiers_versions": [
            (_classifier.id, _classifier.latest_version.version_id)
            for _classifier in classifiers_list
        ],
    }
    return params


@task
async def start_flow_run(
    project_id: int,
    job_type: schemas.ForeignJobType,
    job_source_id: int,
    job_run_id: int,
) -> objects.FlowRun:
    """Start the (inner) flow for the job.

    Args:
        project_id: ID of the project.
        job_type: Type of job to run.
        job_source_id: ID of the source for the job. Corresponds to the table corresponding to
            job_type.
        job_run_id: ID of the row in the job_runs table.
    """
    project_namespace = utils.get_project_namespace(project_id=project_id)
    params = {
        "job_run_id": job_run_id,
        "project_namespace": project_namespace,
    }

    match job_type:
        case schemas.ForeignJobType.gather:
            deployment_name = "gather_flow/gather_flow"
            params = params | get_gather_flow_params(
                project_id=project_id, gather_id=job_source_id
            )
        case schemas.ForeignJobType.classify:
            deployment_name = "classify_flow/classify_flow"
            params = params | get_classify_flow_params(
                project_id=project_id, classifier_id=job_source_id
            )
        case schemas.ForeignJobType.tabulate:
            deployment_name = "tabulate_flow/tabulate_flow"
            params = params | get_tabulate_flow_params(project_id=project_id)
        case schemas.ForeignJobType.delete_gather:
            deployment_name = "delete_gather_flow/delete_gather_flow"
            params = params | {
                "gather_id": job_source_id,
            }
        case schemas.ForeignJobType.gather_classify_tabulate:
            deployment_name = "gather_classify_tabulate_flow/gather_classify_tabulate_flow"
            params = params | get_gather_flow_params(
                project_id=project_id, gather_id=job_source_id
            )
            params = params | get_all_classifiers_params(project_id=project_id)
            params = params | get_tabulate_flow_params(project_id=project_id)
        case schemas.ForeignJobType.classify_tabulate:
            deployment_name = "classify_tabulate_flow/classify_tabulate_flow"
            params = params | get_classify_flow_params(
                project_id=project_id, classifier_id=job_source_id
            )
            params = params | get_tabulate_flow_params(project_id=project_id)
        case schemas.ForeignJobType.delete_gather_tabulate:
            deployment_name = "delete_gather_tabulate_flow/delete_gather_tabulate_flow"
            params = params | get_tabulate_flow_params(project_id=project_id)
        case schemas.ForeignJobType.classifier_archive:
            # Currently the classifier_archive is just a tabulate flow
            # As active_classifiers_versions will be computed based on the non archived
            # classifiers.
            deployment_name = "tabulate_flow/tabulate_flow"
            params = params | get_tabulate_flow_params(project_id=project_id)
        case schemas.ForeignJobType.classifier_restore:
            # Currently the classifier_restore is just a tabulate flow
            # As active_classifiers_versions will be computed based on the non archived
            # classifiers.
            deployment_name = "tabulate_flow/tabulate_flow"
            params = params | get_tabulate_flow_params(project_id=project_id)
        case _:
            raise NotImplementedError(f"Job type {job_type=} not implemented yet.")

    # Add params for composite flows
    match job_type:
        case (
            schemas.ForeignJobType.gather_classify_tabulate
            | schemas.ForeignJobType.classify_tabulate
            | schemas.ForeignJobType.delete_gather_tabulate
        ):
            params = params | {
                "project_id": project_id,
                "job_source_id": job_source_id,
            }

    job_run_flow: objects.FlowRun = await deployments.run_deployment(
        name=deployment_name,
        parameters=params,
        as_subflow=True,
        timeout=0,  # this means it returns immediately with the metadata
        tags=[
            f"project_id:{project_id}",
            f"job_type:{job_type}",
            f"job_source_id:{job_source_id}",
            f"job_run_id:{job_run_id}",
        ],
    )
    return job_run_flow


@task
def job_run_update_started(job_run_id: int) -> None:
    """Update the job_runs row with this (outer) flow's info and set job row status to started.

    Args:
        job_run_id: ID of the row in the job_runs table.
    """
    job_run_update_processing = schemas.JobRunUpdateProcessing(
        id=job_run_id,
    )
    with platform_db.get_session_context() as session:
        job_runs.crud.update_job_run(session=session, job_run_data=job_run_update_processing)


@task
async def wait_for_job_flow_run(job_run_flow_id: uuid.UUID) -> objects.FlowRun:
    """Wait for the inner flow to complete and fetch the final state."""
    logger = prefect.get_run_logger()
    logger.info(f"Waiting for flow run to complete. {job_run_flow_id=}")
    flow_run_result: objects.FlowRun = await flow_runs.wait_for_flow_run(
        flow_run_id=job_run_flow_id
    )
    return flow_run_result


def update_job_run_with_status(job_run_id: int, status: schemas.Status) -> None:
    """Update the job_runs table with the given status."""
    job_run_update_completed = schemas.JobRunUpdateCompleted(id=job_run_id, status=status)
    with platform_db.get_session_context() as session:
        job_runs.crud.update_job_run(session=session, job_run_data=job_run_update_completed)


def get_status_from_flow_run(flow_run: objects.FlowRun) -> schemas.Status:
    """Get the job_runs status from the flow_run.

    This can't be a task other wise prefect will fail.
    """
    assert flow_run.state is not None
    if flow_run.state.is_completed():
        return schemas.Status.completed_successfully
    return schemas.Status.failed


@task
async def job_run_update_completed(job_run_id: int, status: schemas.Status) -> None:
    """Update the job_runs table with the final state of the job (the inner flow)."""
    update_job_run_with_status(job_run_id=job_run_id, status=status)


def non_success_hook(flow: objects.Flow, flow_run: objects.FlowRun, state: objects.State) -> None:
    """Hook to run when the flow fails."""
    job_run_id = flow_run.parameters["job_run_id"]
    update_job_run_with_status(job_run_id=job_run_id, status=schemas.Status.failed)


@flow(
    name="flow_runner_flow",
    on_failure=[non_success_hook],
    on_cancellation=[non_success_hook],
    on_crashed=[non_success_hook],
)
async def flow_runner_flow(
    project_id: int,
    job_type: schemas.ForeignJobType,
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
    job_run_flow = await start_flow_run(
        project_id=project_id,
        job_type=job_type,
        job_source_id=job_source_id,
        job_run_id=job_run_id,
    )
    job_run_update_started(job_run_id=job_run_id)
    # Gottcha you can't pass a flow_run to task or prefect fails the task
    job_run_flow_result = await wait_for_job_flow_run(job_run_flow_id=job_run_flow.id)
    status = get_status_from_flow_run(flow_run=job_run_flow_result)
    # This await is needed or the test does not pass
    await job_run_update_completed(job_run_id=job_run_id, status=status)


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
        name=deployment_name_prefix + flow_runner_flow.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
