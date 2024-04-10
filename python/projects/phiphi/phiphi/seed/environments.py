"""Seed the instances."""
from sqlalchemy.orm import Session

from phiphi.api.environments import crud, schemas

TEST_ENVIRONMENT_CREATE = schemas.EnvironmentCreate(
    name="Phoenix", description="Environment 1", slug="phoenix"
)

TEST_ENVIRONMENT_CREATE_2 = schemas.EnvironmentCreate(
    name="Phoenix", description="Environment 2", slug="phoenix-1234"
)


def seed_test_environment(session: Session) -> None:
    """Seed the environment."""
    environments = [TEST_ENVIRONMENT_CREATE, TEST_ENVIRONMENT_CREATE_2]

    for environment in environments:
        crud.create_environment(session=session, environment=environment)
