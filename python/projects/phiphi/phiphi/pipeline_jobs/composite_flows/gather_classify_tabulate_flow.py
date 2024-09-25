"""Module containing flow which combines gather, run all classifiers, and tabulate flows."""
import asyncio
from typing import Coroutine

import prefect

from phiphi import constants
from phiphi.api.projects import gathers
from phiphi.pipeline_jobs import constants as pipeline_jobs_constants
from phiphi.pipeline_jobs.classify import flow as classify_flow
from phiphi.pipeline_jobs.gathers import flow as gather_flow
from phiphi.pipeline_jobs.tabulate import flow as tabulate_flow


@prefect.flow(name="gather_classify_tabulate_flow")
async def gather_classify_tabulate_flow(
    project_id: int,
    job_source_id: int,
    job_run_id: int,
    project_namespace: str,
    gather_dict: dict,
    gather_child_type: gathers.schemas.ChildTypeName,
    classifiers_dict_list: list[dict],
    class_id_name_map: dict[int, str],
    batch_size: int = pipeline_jobs_constants.DEFAULT_BATCH_SIZE,
) -> None:
    """Flow which gathers, classifies, and tabulates data.

    Note: classify is not implemented yet.
    """
    gather_flow.gather_flow(
        gather_dict=gather_dict,
        gather_child_type=gather_child_type,
        job_run_id=job_run_id,
        project_namespace=project_namespace,
        batch_size=batch_size,
    )

    # For each classifier, classify the data.
    classify_tasks: list[Coroutine] = []
    for classifier_dict in classifiers_dict_list:
        # Running in parallel so that if we are going to run as classifier as a deployment in the
        # future it is an easy change. As well as it being a small optimisation.
        task = asyncio.to_thread(
            classify_flow.classify_flow,
            classifier_dict=classifier_dict,
            job_run_id=job_run_id,
            project_namespace=project_namespace,
        )
        classify_tasks.append(task)
    # Run all tasks (flows) concurrently and capture (and ignore) exceptions.
    # It is important that the gather is not deemed failed if a classifier fails.
    # As otherwise the user will think the gather has not been complete and will re-run.
    # We will find an other way to handle this in the future.
    _ = await asyncio.gather(*classify_tasks, return_exceptions=True)

    tabulate_flow.tabulate_flow(
        class_id_name_map=class_id_name_map,
        job_run_id=job_run_id,
        project_namespace=project_namespace,
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
