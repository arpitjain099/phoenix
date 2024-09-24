"""Recompute all batches and tabulate flow.

This flow is used to recompute all batches and tabulate the data.
"""
from typing import Coroutine, Optional

import prefect

from phiphi import constants
from phiphi.pipeline_jobs import projects
from phiphi.pipeline_jobs.gathers import deduplicate, normalise
from phiphi.pipeline_jobs.tabulate import flow as tabulate_flow


@prefect.flow(name="recompute_all_batches_tabulate_flow")
def recompute_all_batches_tabulate_flow(
    job_run_id: int,
    project_id: int,
    project_namespace: str,
    class_id_name_map: dict[int, str],
    drop_downstream_tables: bool = False,
    gather_ids: Optional[list[int]] = None,
) -> None:
    """Flow that recomputes all batches and tabulates the data.

    Importantly this will not replace any metadata about the normalised batches. Ie `job_run_id`
    will be the original job_run_id from the gather not the new job_run_id.

    This will not run if there are no gather batches to recompute. This is important behaviour
    in that with the deletion of a PI data this will include the gather batches. If a recompute is
    run after a PI delete it will leave all tables and data as is.

    Args:
        job_run_id: The job run ID.
        project_id: The project ID.
        project_namespace: The project namespace.
        class_id_name_map: A dictionary mapping class IDs to class names.
        drop_downstream_tables: If True, delete downstream tables. Defaults to False.
            This will also recompute the schemas for theses downstream tables.
        gather_ids: The gather IDs to recompute. If None, all gather IDs will be recomputed.
    """
    if drop_downstream_tables:
        projects.drop_downstream_tables(
            project_namespace=project_namespace,
        )

    gather_batches_metadata = normalise.get_all_gather_and_job_run_ids(
        bigquery_dataset=project_namespace,
        gather_ids=gather_ids,
    )
    if len(gather_batches_metadata) == 0:
        return None
    for _, gather_batch_metadata in gather_batches_metadata.iterrows():
        normalise.normalise_batches(
            gather_id=gather_batch_metadata.gather_id,
            job_run_id=gather_batch_metadata.job_run_id,
            bigquery_dataset=project_namespace,
        )

    deduplicate.refresh_deduplicated_messages_tables(
        bigquery_dataset=project_namespace,
    )
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
    """Create deployments for recompute_all_batches_tabulate_flow.

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
    task = recompute_all_batches_tabulate_flow.deploy(
        name=deployment_name_prefix + recompute_all_batches_tabulate_flow.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
