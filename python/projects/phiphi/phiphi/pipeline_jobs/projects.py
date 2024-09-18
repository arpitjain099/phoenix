"""Pipeline jobs for projects."""
import prefect
from google import auth
from google.cloud import bigquery

from phiphi import config
from phiphi.pipeline_jobs import constants, create_gcp_table
from phiphi.pipeline_jobs.classify import bq_table_schema as classify_bq_table_schema
from phiphi.pipeline_jobs.tabulate import (
    refresh_gcp_table_schema as tabulate_refresh_gcp_table_schema,
)


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
    # Get the default project for the credentials.
    _, project = auth.default()
    client = bigquery.Client()
    # the dataset reference will use the default project or the project in the project_namespace if
    # has this in the string ie. <project_id>.<dataset_id>
    dataset_reference = bigquery.DatasetReference.from_string(
        dataset_id=project_namespace, default_project=project
    )
    dataset = bigquery.Dataset(dataset_reference)

    dataset.location = config.settings.BQ_DEFAULT_LOCATION
    client.create_dataset(dataset=dataset, exists_ok=True)

    # Create the tabulated table.
    create_gcp_table.create_table(
        table_id=str(dataset_reference.table(constants.TABULATED_MESSAGES_TABLE_NAME)),
        schema_path=tabulate_refresh_gcp_table_schema.get_default_schema_path(),
        with_dummy_rows=with_dummy_rows,
        exists_ok=True,
    )
    # Create classified_messages table.
    create_gcp_table.create_table(
        table_id=str(dataset_reference.table(constants.CLASSIFIED_MESSAGES_TABLE_NAME)),
        schema_path=classify_bq_table_schema.get_path(),
        with_dummy_rows=0,
        exists_ok=True,
    )

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
