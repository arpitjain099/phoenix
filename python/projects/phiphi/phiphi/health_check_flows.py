"""Health check flows."""
from typing import Coroutine

import apify_client
import prefect
import sqlalchemy
from google.api_core import exceptions
from google.cloud import bigquery

from phiphi import config, constants, platform_db, utils


@prefect.task
def check_sqlalchemy_connection() -> bool:
    """Check the SQLAlchemy connection to the database."""
    logger = prefect.get_run_logger()
    try:
        with platform_db.get_session_context() as session:
            # Doing a SELECT 1 to check the connection.
            select_query = sqlalchemy.select(1)
            response = session.execute(select_query)
            result = response.first()
            assert result
            assert result[0] == 1
        logger.info("Successfully connected to platform database.")
        return True
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error(f"Failed to connect to platform database: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    return False


@prefect.task
def check_bigquery_connection() -> bool:
    """Check the BigQuery connection."""
    logger = prefect.get_run_logger()
    try:
        client = bigquery.Client()
        datasets = list(client.list_datasets())
        if datasets:
            logger.info(f"Successfully connected to BigQuery. Found {len(datasets)} datasets.")
        else:
            logger.info("Successfully connected to BigQuery, but no datasets found.")
        return True
    except exceptions.GoogleAPIError as e:
        logger.error(f"Google API Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    return False


@prefect.task
def check_apify_connection() -> bool:
    """Check the Apify connection."""
    logger = prefect.get_run_logger()
    try:
        client = apify_client.ApifyClient(utils.get_apify_api_key())
        actors_collection = client.actors().list()
        actors_count = actors_collection.count
        actors = [item["name"] for item in actors_collection.items]
        if actors_count > 0:
            logger.info(f"Successfully connected to Apify. Found {actors_count} actors.")
            logger.info(f"Actors: {actors}")
        else:
            logger.info("Successfully connected to Apify, but no actors.")
        return True
    except apify_client._errors.ApifyClientError as e:
        logger.error(f"Apify Client Error: {e}")
    except apify_client._errors.ApifyApiError as e:
        logger.error(f"Apify API Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    return False


@prefect.flow
def health_check(environment_slug: str | None) -> None:
    """Main flow for the health check."""
    logger = prefect.get_run_logger()
    logger.info("Health checks started.")
    assert check_sqlalchemy_connection()
    assert check_bigquery_connection()
    assert check_apify_connection()
    logger.info("Health checks completed.")


def create_deployments(
    override_work_pool_name: str | None = None,
    deployment_name_prefix: str = "",
    image: str = constants.DEFAULT_IMAGE,
    tags: list[str] = [],
    build: bool = False,
    push: bool = False,
) -> list[Coroutine]:
    """Create deployments for health check flows.

    By default the deployments are into the main work pool.

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
    environ_slugs = [config.settings.FIRST_ENVIRONMENT_SLUG]
    coroutines = []
    for slug in environ_slugs:
        task = health_check.deploy(
            name=deployment_name_prefix + slug,
            work_pool_name=work_pool_name,
            image=image,
            build=build,
            push=push,
            tags=tags,
            parameters={"environment_slug": slug},
        )
        coroutines.append(task)

    return coroutines
