"""Module containing the Prefect flow for gathers."""
from typing import Coroutine

import prefect

from phiphi import constants
from phiphi.api.projects import gathers
from phiphi.pipeline_jobs import constants as pipeline_jobs_constants
from phiphi.pipeline_jobs.gathers import apify_scrape, deduplicate, delete, normalise


@prefect.flow(name="gather_flow")
def gather_flow(
    gather_dict: dict,
    gather_child_type: gathers.schemas.ChildTypeName,
    job_run_id: int,
    project_namespace: str,
    batch_size: int = pipeline_jobs_constants.DEFAULT_BATCH_SIZE,
    batch_of_batches_size: int = pipeline_jobs_constants.DEFAULT_BATCH_OF_BATCHES_SIZE,
) -> None:
    """Flow which gathers data.

    Args:
        gather_dict (dict): Dictionary containing the gather parameters.
        gather_child_type (gathers.schemas.ChildTypeName): The type of gather.
        job_run_id (int): The job run id.
        project_namespace (str): The project namespace.
        batch_size (int, optional): The batch size. Defaults to
            pipeline_jobs_constants.DEFAULT_BATCH_SIZE. Note that one batch is written to one row
            in BigQuery, and BQ has a row size limit of 10MB.
        batch_of_batches_size (int, optional): The number of batches to read and process at once
            when normalising.

    Warning: there is a race condition in this flow for the deduplicate step if multiple gathers
    flow are being run at the same time. Very unlikely though.
    """
    # Create the gather object from the gather_dict as prefect can't parse it automatically from
    # the parameters
    gather = gathers.child_types.get_response_type(gather_child_type)(**gather_dict)

    scrape_response = apify_scrape.apify_scrape_and_batch_download_results(
        gather=gather,
        job_run_id=job_run_id,
        bigquery_dataset=project_namespace,
        batch_size=batch_size,
    )
    # If nothing has been scraped then there is no need to normalise.
    # This is important because the table is only created when scrape processes results
    # the normalise will throw an error if the table does not exist.
    # We could have the Apify scrape insert a gather batch that is empty but then this
    # creates the wrong schema for the generalised_messages table.
    if scrape_response.total_items == 0:
        return
    normalise.normalise_batches(
        gather_job_run_pairs=[(gather.id, job_run_id)],
        bigquery_dataset=project_namespace,
        batch_of_batches_size=batch_of_batches_size,
    )
    deduplicate.refresh_deduplicated_messages_tables(
        bigquery_dataset=project_namespace,
    )
    deduplicate.refresh_deduplicated_authors_tables(
        bigquery_dataset=project_namespace,
    )


@prefect.flow(name="delete_gather_flow")
def delete_flow(
    gather_id: int,
    # To be consistent with other flows we keep the job_run_id even though it is not used.
    job_run_id: int,
    project_namespace: str,
) -> None:
    """Flow which deletes gathered data."""
    delete.delete_gathered_data(
        gather_id=gather_id,
        bigquery_dataset=project_namespace,
    )
    deduplicate.refresh_deduplicated_messages_tables(
        bigquery_dataset=project_namespace,
    )
    deduplicate.refresh_deduplicated_authors_tables(
        bigquery_dataset=project_namespace,
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

    task_2 = delete_flow.deploy(
        name=deployment_name_prefix + delete_flow.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task, task_2]
