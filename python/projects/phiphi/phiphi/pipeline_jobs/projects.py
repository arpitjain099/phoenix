"""Pipeline jobs for projects."""
from enum import Enum
from typing import Coroutine

import prefect
from google.cloud import bigquery

from phiphi import config, constants, project_db, utils
from phiphi.pipeline_jobs import constants as pipeline_constants
from phiphi.pipeline_jobs import tabulated_messages
from phiphi.pipeline_jobs.composite_flows import recompute_all_batches_tabulate_flow


@prefect.task
def init_project_db(
    project_namespace: str,
    workspace_slug: str,
    with_dummy_data: bool = False,
) -> str:
    """Initialize the project database.

    This task will be combined in to a flow to initialise other project resources.
    IE. superset dashboards.

    Args:
        project_namespace (str): The project namespace.
        workspace_slug (str): The workspace_slug.
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
    dataset.labels = {"workspace_slug": workspace_slug}
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
        DROP TABLE {project_namespace}.{pipeline_constants.GENERALISED_MESSAGES_TABLE_NAME}
    """
    client.query(query)
    return None


class RecomputeStrategy(str, Enum):
    """Recompute strategy enum."""

    always = "always"
    never = "never"
    on_upgrade = "on_upgrade"


@prefect.flow(name="project_apply_migrations")
def project_apply_migrations(
    job_run_id: int,
    project_id: int,
    project_namespace: str,
    active_classifiers_versions: list[tuple[int, int]],
    with_recompute_all_batches: RecomputeStrategy = RecomputeStrategy.on_upgrade,
) -> bool:
    """Apply the migrations to the project database.

    If the migrations are applied successfully then the recompute_all_batches_tabulate_flow will be
    run.

    Args:
        job_run_id (int): The job run id.
        project_id (int): The project id.
        project_namespace (str): The project namespace.
        active_classifiers_versions (list[tuple[int, int]]): The active classifiers versions to
            use. Each tuple should be (classifier_id, version_id).
        with_recompute_all_batches (RecomputeStrategy, optional): The recompute strategy.
            Defaults to RecomputeStrategy.on_upgrade.
    """
    logger = prefect.get_run_logger()
    with project_db.init_connection(
        project_db.form_bigquery_sqlalchmey_uri(project_namespace)
    ) as connection:
        logger.info("Applying migrations.")
        revisions_applied = project_db.alembic_upgrade(connection)
        logger.info(f"Revisions applied: {revisions_applied}")
    if with_recompute_all_batches == RecomputeStrategy.always or (
        with_recompute_all_batches == RecomputeStrategy.on_upgrade and revisions_applied
    ):
        recompute_all_batches_tabulate_flow.recompute_all_batches_tabulate_flow(
            job_run_id=job_run_id,
            project_id=project_id,
            project_namespace=project_namespace,
            active_classifiers_versions=active_classifiers_versions,
            # It is important that we drop the downstream tables as the schemas of downstream
            # tables may have changed.
            drop_downstream_tables=True,
        )
        logger.info("Recompute all batches tabulate flow completed.")
    logger.info("Migrations applied.")
    return revisions_applied


def create_deployments(
    override_work_pool_name: str | None = None,
    deployment_name_prefix: str = "",
    image: str = constants.DEFAULT_IMAGE,
    tags: list[str] = [],
    build: bool = False,
    push: bool = False,
) -> list[Coroutine]:
    """Create deployments for projects.

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
    task = project_apply_migrations.deploy(
        name=deployment_name_prefix + project_apply_migrations.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
