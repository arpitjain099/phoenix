"""Recompute all batches and tabulate flow.

This flow is used to recompute all batches and tabulate the data.
"""
import prefect

from phiphi.api.projects import gathers


@prefect.task(name="recompute_all_batches_tabulate_flow")
def recompute_all_batches_tabulate_flow(
    project_id: int,
    job_run_id: int,
    project_namespace: str,
    gathers_dict_list: list[dict],
    gather_child_type_list: list[gathers.schemas.ChildTypeName],
    class_id_name_map: dict[int, str],
) -> None:
    """Flow that recomputes all batches and tabulates the data.

    Args:
        project_id: The project ID.
        job_run_id: The job run ID.
        project_namespace: The project namespace.
        gathers_dict_list: A list of gather dictionaries that will be recomputed
        gather_child_type_list: A list of gather child types for the gathers_dict_list. The index
            of the gather child type has to match the index of the gather dictionary in the
            gathers_dict_list.
        class_id_name_map: A dictionary mapping class IDs to class names.
    """
    # For each gather normalise the data
    # Run deduplicate flow
    # Run tabulate flow
    pass
