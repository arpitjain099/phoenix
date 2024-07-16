"""Module containing flow which combines gather, run all classifiers, and tabulate flows."""

from typing import Coroutine

import prefect

from phiphi import constants
from phiphi.api.projects import gathers, job_runs
from phiphi.pipeline_jobs import utils as pipeline_jobs_utils


@prefect.flow(name="gather_classify_tabulate_flow")
async def gather_classify_tabulate_flow(
    project_id: int,
    job_source_id: int,
    job_run_id: int,
    project_namespace: str,
    gather_dict: dict,
    gather_child_type: gathers.schemas.ChildTypeName,
    batch_size: int = 100,
) -> None:
    """Flow which gathers, classifies, and tabulates data.

    Note: classify is not implemented yet.
    """
    await pipeline_jobs_utils.run_flow_deployment_as_subflow(
        deployment_name="gather_flow/gather_flow",
        flow_params={
            "gather_dict": gather_dict,
            "gather_child_type": gather_child_type,
            "job_run_id": job_run_id,
            "project_namespace": project_namespace,
            "batch_size": batch_size,
        },
        project_id=project_id,
        job_type=job_runs.schemas.ForeignJobType.gather,
        job_source_id=job_source_id,
        job_run_id=job_run_id,
    )

    # For each active classifier, classify the data.

    await pipeline_jobs_utils.run_flow_deployment_as_subflow(
        deployment_name="tabulate_flow/tabulate_flow",
        flow_params={
            "job_run_id": job_run_id,
            "project_namespace": project_namespace,
        },
        project_id=project_id,
        job_type=job_runs.schemas.ForeignJobType.tabulate,
        job_source_id=job_source_id,
        job_run_id=job_run_id,
    )


def create_deployments(
    override_work_pool_name: str | None = None,
    deployment_name_prefix: str = "",
    image: str = constants.DEFAULT_IMAGE,
    tags: list[str] = [],
    build: bool = False,
    push: bool = False,
) -> list[Coroutine]:
    """Create deployments for gather_classify_tabulate_flow.

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
    task = gather_classify_tabulate_flow.deploy(
        name=deployment_name_prefix + gather_classify_tabulate_flow.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
