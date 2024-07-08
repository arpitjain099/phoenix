"""Seed the projects."""
from sqlalchemy.orm import Session

from phiphi.api.projects import crud, schemas

TEST_PROJECT_CREATE = schemas.ProjectCreate(
    name="Phoenix Project 1",
    description="Project 1",
    workspace_slug="main",
    pi_deleted_after_days=90,
    delete_after_days=20,
    expected_usage=schemas.ExpectedUsage.weekly,
)

TEST_PROJECT_CREATE_2 = schemas.ProjectCreate(
    name="Phoenix Project 2",
    description="Project 2",
    workspace_slug="main",
    pi_deleted_after_days=90,
    delete_after_days=20,
    expected_usage=schemas.ExpectedUsage.monthly,
)

TEST_PROJECT_CREATE_3 = schemas.ProjectCreate(
    name="Phoenix Project 3",
    description="Project 3",
    workspace_slug="test",
    pi_deleted_after_days=90,
    delete_after_days=20,
    expected_usage=schemas.ExpectedUsage.weekly,
)

TEST_PROJECT_CREATE_4_DELETED = schemas.ProjectCreate(
    name="Phoenix Project 3",
    description="Project 3",
    workspace_slug="test",
    pi_deleted_after_days=90,
    delete_after_days=20,
    expected_usage=schemas.ExpectedUsage.weekly,
)


def seed_test_project(session: Session) -> None:
    """Seed the project."""
    projects = [
        TEST_PROJECT_CREATE,
        TEST_PROJECT_CREATE_2,
        TEST_PROJECT_CREATE_3,
        TEST_PROJECT_CREATE_4_DELETED,
    ]

    for project in projects:
        crud.create_project(session=session, project=project)

    crud.delete_project(session=session, project_id=4)
