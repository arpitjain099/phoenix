"""Pipeline jobs for projects."""
import prefect
from google.cloud import bigquery

from phiphi import config, project_db, utils
from phiphi.pipeline_jobs import constants, tabulated_messages
from phiphi.pipeline_jobs.composite_flows import recompute_all_batches_tabulate_flow


@prefect.task
def init_project_db(
    project_namespace: str,
    with_dummy_data: bool = False,
) -> str:
    """Initialize the project database.

    This task will be combined in to a flow to initialise other project resources.
    IE. superset dashboards.

    Args:
        project_namespace (str): The project namespace.
        with_dummy_data (bool, optional): If True then dummy data will be seeded.
            Defaults to False.

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
        if with_dummy_data:
            tabulated_messages.seed_dummy_data(project_namespace)

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


@prefect.flow(name="project_apply_migrations")
def project_apply_migrations(
    job_run_id: int,
    project_id: int,
    class_id_name_map: dict[int, str],
    project_namespace: str,
) -> bool:
    """Apply the migrations to the project database.

    If the migrations are applied successfully then the recompute_all_batches_tabulate_flow will be
    run.

    Args:
        job_run_id (int): The job run ID.
        project_id (int): The project ID.
        class_id_name_map (dict[int, str]): A dictionary mapping class IDs to class names.
        project_namespace (str): The project namespace.

    Returns:
        bool: True if the migrations were applied successfully.
    """
    with project_db.init_connection(
        project_db.form_bigquery_sqlalchmey_uri(project_namespace)
    ) as connection:
        revisions_applyed = project_db.alembic_upgrade(connection)
    if revisions_applyed:
        recompute_all_batches_tabulate_flow.recompute_all_batches_tabulate_flow(
            job_run_id=job_run_id,
            project_id=project_id,
            project_namespace=project_namespace,
            class_id_name_map=class_id_name_map,
            # It is important that we drop the downstream tables as the schemas of downstream
            # tables may have changed.
            drop_downstream_tables=True,
        )
    return revisions_applyed
