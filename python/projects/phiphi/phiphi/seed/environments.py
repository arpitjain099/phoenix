"""Seed the environments."""
from sqlalchemy.orm import Session

from phiphi import config
from phiphi.api.environments import crud, schemas

TEST_ENVIRONMENT_CREATE = schemas.EnvironmentCreate(
    name="Phoenix", description="Environment 1", slug="phoenix"
)

TEST_ENVIRONMENT_CREATE_2 = schemas.EnvironmentCreate(
    name="Test", description="Testing seed", slug="test"
)


def seed_test_environment(session: Session) -> None:
    """Seed the environment."""
    environments = [TEST_ENVIRONMENT_CREATE, TEST_ENVIRONMENT_CREATE_2]

    for environment in environments:
        crud.create_environment(session=session, environment=environment)


def init_main_environment(session: Session) -> schemas.EnvironmentResponse:
    """Create the first environment."""
    environment = crud.get_environment(session, "main")
    if not environment:
        environment_in = schemas.EnvironmentCreate(
            name=config.settings.FIRST_ENVIRONMENT_NAME,
            description=config.settings.FIRST_ENVIRONMENT_DESCRIPTION,
            slug=config.settings.FIRST_ENVIRONMENT_SLUG,
        )
        environment = crud.create_environment(session=session, environment=environment_in)
    return environment
