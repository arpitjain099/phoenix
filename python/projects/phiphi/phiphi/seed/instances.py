"""Seed the instances."""
from sqlalchemy.orm import Session

from phiphi.api.instances import crud, schemas

TEST_INSTANCE_CREATE = schemas.InstanceCreate(
    name="Phoenix Instance 1",
    description="Instance 1",
    environment_key=schemas.EnvironmentKey.main,
    pi_deleted_after_days=90,
    delete_after_days=20,
    expected_usage="average",
)

TEST_INSTANCE_CREATE_2 = schemas.InstanceCreate(
    name="Phoenix Instance 2",
    description="Instance 2",
    environment_key=schemas.EnvironmentKey.main,
    pi_deleted_after_days=90,
    delete_after_days=20,
    expected_usage="average",
)


def seed_test_instance(session: Session) -> None:
    """Seed the instance."""
    instances = [TEST_INSTANCE_CREATE, TEST_INSTANCE_CREATE_2]

    for instance in instances:
        crud.create_instance(session=session, instance=instance)
