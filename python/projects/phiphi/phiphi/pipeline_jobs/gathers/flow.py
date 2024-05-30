"""Module containing the Prefect flow for gathers."""
from typing import Coroutine

import prefect

from phiphi import constants
from phiphi.pipeline_jobs.gathers import apify_input_schemas, apify_scrape


@prefect.flow(name="gather_flow")
def gather_flow(
    run_input: apify_input_schemas.ApifyInputType,
    project_id: int,
    gather_id: int,
    job_run_id: int,
    bigquery_dataset: str,
    bigquery_table: str,
    batch_size: int = 100,
) -> None:
    """Flow which gathers data."""
    apify_scrape.apify_scrape_and_batch_download_results(
        run_input=run_input,
        project_id=project_id,
        gather_id=gather_id,
        job_run_id=job_run_id,
        bigquery_dataset=bigquery_dataset,
        bigquery_table=bigquery_table,
        batch_size=batch_size,
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
