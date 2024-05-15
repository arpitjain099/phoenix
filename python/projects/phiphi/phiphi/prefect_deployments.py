"""Deployments creation entry point.

To add new deployments, add the create_deployments function to variable
`list_of_create_deployment_fn`.
The functions in this list have the same interface as the CreateDeployments protocol.
"""
from typing import Coroutine, Protocol

from phiphi import constants, hello_flows


class CreateDeploymentsInterface(Protocol):
    """Protocol for create deployments functions."""

    def __call__(
        self,
        override_work_pool_name: str | None = None,
        deployment_name_prefix: str = "",
        image: str = constants.DEFAULT_IMAGE,
        tags: list[str] = [],
        build: bool = False,
        push: bool = False,
    ) -> list[Coroutine]:
        """Create deployments interface."""
        pass


list_of_create_deployment_fn: list[CreateDeploymentsInterface] = [hello_flows.create_deployments]
