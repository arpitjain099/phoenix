"""Hello world flow for testing.

This is a toy example and should be delete once a real flow is created.
"""
from typing import Coroutine

import prefect

from phiphi import constants


@prefect.flow
def hello(hello_name: str = "Benjamin") -> None:
    """Prints a greeting to the provided name."""
    logger = prefect.get_run_logger()
    logger.info(f"Hello, {hello_name}!")


def create_deployments(
    override_work_pool_name: str | None = None,
    deployment_name_prefix: str = "",
    image: str = constants.DEFAULT_IMAGE,
    tags: list[str] = [],
    build: bool = False,
    push: bool = False,
) -> list[Coroutine]:
    """Create deployments for hello world flows.

    Creates the default and john deployments for the hello world flow.

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
    names = ["default", "john"]
    coroutines = []
    for name in names:
        task = hello.deploy(
            name=deployment_name_prefix + name,
            work_pool_name=work_pool_name,
            image=image,
            build=build,
            push=push,
            tags=tags,
            parameters={"hello_name": name},
        )
        coroutines.append(task)

    return coroutines
