"""Pipeline jobs for projects."""
import prefect
from google.cloud import bigquery

from phiphi import utils


@prefect.task
def init_project_db(
    project_id: int,
    namespace_prefix: str = "",
) -> str:
    """Initialize the project database.

    This task will be combined in to a flow to initialise other project resources.
    IE. superset dashboards.

    Args:
        project_id (int): The project id.
        namespace_prefix (str, optional): The namespace prefix. Defaults to "".
            Used for testing.

    Returns:
        str: The project namespace.
    """
    client = bigquery.Client()
    project_namespace = utils.get_project_namespace(project_id, namespace_prefix)
    client.create_dataset(dataset=project_namespace, exists_ok=True)
    return project_namespace
