"""Recompute all batches and tabulate flow.

This flow is used to recompute all batches and tabulate the data.
"""
import prefect

from phiphi.api.projects import gathers
from phiphi.pipeline_jobs.gathers import deduplicate, normalise
from phiphi.pipeline_jobs.tabulate import flow as tabulate_flow


@prefect.task(name="recompute_all_batches_tabulate_flow")
def recompute_all_batches_tabulate_flow(
    project_id: int,
    gather_job_run_ids: list[int],
    project_namespace: str,
    gathers_dict_list: list[dict],
    gather_child_type_list: list[gathers.schemas.ChildTypeName],
    class_id_name_map: dict[int, str],
) -> None:
    """Flow that recomputes all batches and tabulates the data.

    It is important that you keep the `gather_job_run_ids`, `gathers_dict_list`, and
    `gather_child_type_list` in the same order as they are all related to each other.

    Be aware a gather can have multiple gather job runs. This is why we have a list of
    gather_job_run_ids.


    Args:
        project_id: The project ID.
        project_namespace: The project namespace.
        gather_job_run_ids: A list of gather job run IDs. The index of the gather job run ID has to
        match the index of the gather dictionary in the gathers_dict_list.
        gathers_dict_list: A list of gather dictionaries that will be recomputed
        gather_child_type_list: A list of gather child types for the gathers_dict_list. The index
            of the gather child type has to match the index of the gather dictionary in the
            gathers_dict_list.
        class_id_name_map: A dictionary mapping class IDs to class names.
    """
    for job_run_id, gather_dict, gather_child_type in zip(
        gather_job_run_ids, gathers_dict_list, gather_child_type_list
    ):
        gather = gathers.child_types.get_response_type(gather_child_type)(**gather_dict)
        normalise.normalise_batches(
            gather=gather,
            job_run_id=job_run_id,
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
