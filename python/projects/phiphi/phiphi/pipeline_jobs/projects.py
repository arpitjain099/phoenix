"""Pipeline jobs for projects."""
import prefect
from google.cloud import bigquery

from phiphi import config, project_db, utils
from phiphi.pipeline_jobs import constants, tabulated_messages


@prefect.task
def init_project_db(
    project_namespace: str,
    with_dummy_rows: int = 0,
) -> str:
    """Initialize the project database.

    This task will be combined in to a flow to initialise other project resources.
    IE. superset dashboards.

    Args:
        project_namespace (str): The project namespace.
        with_dummy_rows (int): The number of dummy rows to insert into the table.

    Returns:
        str: The project namespace.
    """
    project = utils.get_default_bigquery_project()
    client = bigquery.Client()
    # the dataset reference will use the default project or the project in the project_namespace if
    # has this in the string ie. <project_id>.<dataset_id>
    dataset_reference = bigquery.DatasetReference.from_string(
        dataset_id=project_namespace, default_project=project
    )
    dataset = bigquery.Dataset(dataset_reference)

    dataset.location = config.settings.BQ_DEFAULT_LOCATION
    client.create_dataset(dataset=dataset, exists_ok=True)

    with project_db.init_connection(
        project_db.form_bigquery_sqlalchmey_uri(project_namespace)
    ) as connection:
        project_db.alembic_upgrade(connection)
        if with_dummy_rows:
            tabulated_messages.seed_dummy_data(connection)

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


@prefect.task
def drop_downstream_tables(
    project_namespace: str,
) -> None:
    """Drop downstream tables.

    Currently this only drops the generalised_messages table as the rest of the tables are
    recreated with each pipeline.

    Args:
        project_namespace (str): The project namespace.
    """
    client = bigquery.Client()
    query = f"""
        DROP TABLE {project_namespace}.{constants.GENERALISED_MESSAGES_TABLE_NAME}
    """
    client.query(query)
    return None
