"""Recompute all batches and tabulate flow.

This flow is used to recompute all batches and tabulate the data.
"""
import prefect

from phiphi.pipeline_jobs import projects
from phiphi.pipeline_jobs.gathers import deduplicate, normalise
from phiphi.pipeline_jobs.tabulate import flow as tabulate_flow


@prefect.task(name="recompute_all_batches_tabulate_flow")
def recompute_all_batches_tabulate_flow(
    job_run_id: int,
    project_id: int,
    project_namespace: str,
    class_id_name_map: dict[int, str],
    drop_downstream_tables: bool = False,
) -> None:
    """Flow that recomputes all batches and tabulates the data.

    Importantly this will not replace any metadata about the normalised batches. Ie `job_run_id`
    will be the original job_run_id from the gather not the new job_run_id.

    Args:
        job_run_id: The job run ID.
        project_id: The project ID.
        project_namespace: The project namespace.
        class_id_name_map: A dictionary mapping class IDs to class names.
        drop_downstream_tables: If True, delete downstream tables. Defaults to False.
            This will also recompute the schemas for theses downstream tables.
    """
    if drop_downstream_tables:
        projects.drop_downstream_tables(
            project_namespace=project_namespace,
        )

    gather_batches_metadata = normalise.get_gather_batches_metadata(
        bigquery_dataset=project_namespace
    )
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
