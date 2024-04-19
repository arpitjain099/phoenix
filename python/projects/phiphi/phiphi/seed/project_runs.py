"""Seed the project runs."""
from sqlalchemy.orm import Session

from phiphi.api.projects.project_runs import crud


def seed_test_project_runs(session: Session) -> None:
    """Seed the project runs."""
    for num in range(1, 3):
        crud.create_project_runs(session=session, project_id=num)
