"""Pipeline jobs for projects."""
import prefect
from google.cloud import bigquery


@prefect.task
def init_project_db(
    project_namespace: str,
) -> str:
    """Initialize the project database.

    This task will be combined in to a flow to initialise other project resources.
    IE. superset dashboards.

    Args:
        project_namespace (str): The project namespace.

    Returns:
        str: The project namespace.
    """
    client = bigquery.Client()
    client.create_dataset(dataset=project_namespace, exists_ok=True)
    return project_namespace


@prefect.task
def delete_project_db(
    project_namespace: str,
) -> None:
    """Delete the project database.

    Args:
        project_namespace (str): The project namespace.
    """
    client = bigquery.Client()
    client.delete_dataset(dataset=project_namespace, delete_contents=True, not_found_ok=True)
