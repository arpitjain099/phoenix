"""Test Projects."""
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.api.projects import models


def test_project_seeded(session: sqlalchemy.orm.Session, reseed_tables) -> None:
    """Test that the database is seeded."""
    response = session.execute(
        sqlalchemy.select(sqlalchemy.func.count()).select_from(models.Project)
    )
    count = response.one()
    assert count
    assert count[0] == 3


CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_project(reseed_tables, client: TestClient) -> None:
    """Test create and then get of an project."""
    data = {
        "name": "first project",
        "description": "Project 1",
        "environment_slug": "main",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "weekly",
    }
    response = client.post("/projects/", json=data)
    assert response.status_code == 200
    project = response.json()
    assert project["name"] == data["name"]
    assert project["description"] == data["description"]
    assert project["environment_slug"] == data["environment_slug"]
    assert project["pi_deleted_after_days"] == data["pi_deleted_after_days"]
    assert project["delete_after_days"] == data["delete_after_days"]
    assert project["expected_usage"] == data["expected_usage"]
    assert project["created_at"] == CREATED_TIME

    response = client.get(f"/projects/{project['id']}")
    assert response.status_code == 200

    project = response.json()

    assert project["name"] == data["name"]
    assert project["description"] == data["description"]
    assert project["created_at"] == CREATED_TIME
    assert project["environment_slug"] == data["environment_slug"]
    assert project["pi_deleted_after_days"] == data["pi_deleted_after_days"]
    assert project["delete_after_days"] == data["delete_after_days"]


def test_get_project_not_found(client: TestClient, recreate_tables) -> None:
    """Test getting an project that does not exist."""
    response = client.get("/projects/5")
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_get_projects(client: TestClient, reseed_tables) -> None:
    """Test getting projects."""
    response = client.get("/projects/")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 3


def test_get_projects_pagination(client: TestClient, reseed_tables) -> None:
    """Test getting users with pagination."""
    response = client.get("/projects/?start=1&end=1")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["id"] == 2


@pytest.mark.freeze_time(UPDATE_TIME)
def test_update_project(
    client: TestClient, reseed_tables, session: sqlalchemy.orm.Session
) -> None:
    """Test updating an project."""
    data = {"description": "New project"}
    project_id = 1
    response = client.put(f"/projects/{project_id}", json=data)
    assert response.status_code == 200
    project = response.json()
    assert project["description"] == data["description"]
    db_project = session.get(models.Project, project_id)
    assert db_project
    assert db_project.description == data["description"]
    assert db_project.updated_at.isoformat() == UPDATE_TIME


def test_update_project_not_found(client: TestClient, recreate_tables) -> None:
    """Test updating an project that does not exist."""
    data = {"description": "New project"}
    response = client.put("/projects/100", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_environment_defaults_main(client: TestClient, reseed_tables) -> None:
    """Test that environment defaults to main, when nothing is passed as parameter."""
    data = {
        "name": "first project",
        "description": "Project 1",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "one_off",
    }
    response = client.post("/projects/", json=data)
    assert response.status_code == 200
    project = response.json()
    assert project["environment_slug"] == "main"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_project_with_non_existing_env(recreate_tables, client: TestClient) -> None:
    """Test create and then get of an project."""
    data = {
        "name": "first project",
        "description": "Project 1",
        "environment_slug": "non-existing",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "weekly",
    }
    response = client.post("/projects/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Environment not found"}
