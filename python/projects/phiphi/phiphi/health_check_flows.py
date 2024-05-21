"""Health check flows."""
import logging
from typing import Coroutine

import prefect

from phiphi import config, constants

logger = logging.getLogger(__name__)


@prefect.flow
def health_check(environment_slug: str | None) -> None:
    """Main flow for the health check."""
    logger.info("Health checks started.")
    assert True
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
