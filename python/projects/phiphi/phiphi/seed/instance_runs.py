"""Seed the instance runs."""
from sqlalchemy.orm import Session

from phiphi.api.instances.instance_runs import crud


def seed_test_instance_runs(session: Session) -> None:
    """Seed the instance runs."""
    for num in range(1, 3):
        crud.create_instance_runs(session=session, instance_id=num)
