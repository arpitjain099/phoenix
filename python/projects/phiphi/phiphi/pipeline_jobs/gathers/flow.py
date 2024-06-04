"""Module containing the Prefect flow for gathers."""
from typing import Coroutine

import prefect

from phiphi import constants, utils
from phiphi.api.projects import gathers
from phiphi.pipeline_jobs.gathers import apify_scrape, normalisers


@prefect.flow(name="gather_flow")
def gather_flow(
    gather: gathers.schemas.GatherResponse,
    job_run_id: int,
    batch_size: int = 100,
) -> None:
    """Flow which gathers data."""
    bigquery_dataset = utils.get_project_namespace(project_id=gather.project_id)

    apify_scrape.apify_scrape_and_batch_download_results(
        gather=gather,
        job_run_id=job_run_id,
        bigquery_dataset=bigquery_dataset,
        batch_size=batch_size,
    )
    normalisers.normalise_batches(
        gather=gather,
        job_run_id=job_run_id,
        bigquery_dataset=bigquery_dataset,
    )


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
    task = gather_flow.deploy(
        name=deployment_name_prefix + gather_flow.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
