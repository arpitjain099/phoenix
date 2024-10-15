"""Test Projects."""
from unittest import mock

import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.api.projects import crud, models


def test_project_seeded(session: sqlalchemy.orm.Session, reseed_tables) -> None:
    """Test that the database is seeded."""
    response = session.execute(
        sqlalchemy.select(sqlalchemy.func.count()).select_from(models.Project)
    )
    count = response.one()
    assert count
    # One is deleted
    assert count[0] == 4


CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.patch_settings({"USE_MOCK_BQ": False})
@mock.patch("phiphi.pipeline_jobs.projects.delete_project_db")
@mock.patch("phiphi.pipeline_jobs.projects.init_project_db")
@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_delete_project(
    mock_project_init_db, mock_delete_db, reseed_tables, client: TestClient, patch_settings
) -> None:
    """Test create and then get of an project."""
    data = {
        "name": "first project",
        "description": "Project 1",
        "workspace_slug": "main",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "weekly",
    }
    response = client.post("/projects/", json=data)
    assert response.status_code == 200
    project = response.json()
    assert project["name"] == data["name"]
    assert project["description"] == data["description"]
    assert project["workspace_slug"] == data["workspace_slug"]
    assert project["pi_deleted_after_days"] == data["pi_deleted_after_days"]
    assert project["delete_after_days"] == data["delete_after_days"]
    assert project["expected_usage"] == data["expected_usage"]
    assert project["created_at"] == CREATED_TIME
    assert project["last_job_run_completed_at"] is None
    assert project["latest_job_run"] is None
    assert project["checked_problem_statement"] is False
    assert project["checked_sources"] is False
    assert project["checked_gather"] is False
    assert project["checked_classify"] is False
    assert project["checked_visualise"] is False
    assert project["checked_explore"] is False

    mock_project_init_db.assert_called_once_with(
        f"project_id{project['id']}", "main", with_dummy_data=True
    )

    response = client.get(f"/projects/{project['id']}")
    assert response.status_code == 200

    project = response.json()

    assert project["name"] == data["name"]
    assert project["description"] == data["description"]
    assert project["created_at"] == CREATED_TIME
    assert project["workspace_slug"] == data["workspace_slug"]
    assert project["pi_deleted_after_days"] == data["pi_deleted_after_days"]
    assert project["delete_after_days"] == data["delete_after_days"]
    assert project["last_job_run_completed_at"] is None
    assert project["latest_job_run"] is None

    response = client.get("/projects/")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 4

    response = client.delete(f"/projects/{project['id']}")
    assert response.status_code == 200
    mock_delete_db.assert_called_once_with(f"project_id{project['id']}")

    response = client.get(f"/projects/{project['id']}")
    assert response.status_code == 404

    response = client.get("/projects/")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 3


@pytest.mark.patch_settings({"USE_MOCK_BQ": False})
@mock.patch("phiphi.pipeline_jobs.projects.init_project_db")
def test_create_project_error_init(
    mock_project_init_db, reseed_tables, client: TestClient, session, patch_settings
) -> None:
    """Test create project if there is an error in init_project_db."""
    project_list = crud.get_projects(session=session)
    mock_project_init_db.side_effect = ValueError("Error")
    data = {
        "name": "first project",
        "description": "Project 1",
        "workspace_slug": "main",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "weekly",
    }
    response = client.post("/projects/", json=data)
    mock_project_init_db.assert_called_once()
    assert response.status_code == 500
    project_list_after_failed_create = crud.get_projects(session=session)
    assert len(project_list) == len(project_list_after_failed_create)


@pytest.mark.patch_settings({"USE_MOCK_BQ": False})
@mock.patch("phiphi.pipeline_jobs.projects.delete_project_db")
def test_delete_project_error_init(
    mock_project_delete_db, reseed_tables, client: TestClient, session, patch_settings
) -> None:
    """Test delete project if there is an error in delete_project_db."""
    project_list = crud.get_projects(session=session)
    mock_project_delete_db.side_effect = ValueError("Error")
    response = client.delete("/projects/1")
    mock_project_delete_db.assert_called_once()
    assert response.status_code == 500
    project_list_after_failed_delete = crud.get_projects(session=session)
    assert len(project_list) == len(project_list_after_failed_delete)


@mock.patch("phiphi.pipeline_jobs.projects.init_project_db")
@pytest.mark.patch_settings({"USE_MOCK_BQ": True})
def test_create_project_mock_bq(
    mock_project_init_db, reseed_tables, client: TestClient, session, patch_settings
) -> None:
    """Test create project if there is an error in init_project_db."""
    mock_project_init_db.side_effect = ValueError("Error")
    data = {
        "name": "first project",
        "description": "Project 1",
        "workspace_slug": "main",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "weekly",
    }
    response = client.post("/projects/", json=data)
    mock_project_init_db.assert_not_called()
    assert response.status_code == 200


@pytest.mark.patch_settings({"USE_MOCK_BQ": True})
@mock.patch("phiphi.pipeline_jobs.projects.delete_project_db")
def test_delete_project_mock_bq(
    mock_project_delete_db, reseed_tables, client: TestClient, session, patch_settings
) -> None:
    """Test delete project if there is an error in delete_project_db."""
    mock_project_delete_db.side_effect = ValueError("Error")
    response = client.delete("/projects/1")
    mock_project_delete_db.assert_not_called()
    assert response.status_code == 200


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
    assert projects[0]["id"] == 3
    assert projects[1]["id"] == 2
    assert projects[2]["id"] == 1

    # The list projects should not get the job data
    assert "latest_job_run" not in projects[0]
    assert "last_job_run_completed_at" not in projects[0]


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
    data = {"description": "New project", "checked_problem_statement": True}
    project_id = 1
    response = client.put(f"/projects/{project_id}", json=data)
    assert response.status_code == 200
    project = response.json()
    assert project["description"] == data["description"]
    orm_project = session.get(models.Project, project_id)
    assert orm_project
    assert orm_project.description == data["description"]
    assert orm_project.checked_problem_statement is True
    assert orm_project.updated_at.isoformat() == UPDATE_TIME


def test_update_project_not_found(client: TestClient, recreate_tables) -> None:
    """Test updating an project that does not exist."""
    data = {"description": "New project"}
    response = client.put("/projects/100", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


@mock.patch("phiphi.pipeline_jobs.projects.init_project_db")
def test_workspace_defaults_main(mock_project_init_db, client: TestClient, reseed_tables) -> None:
    """Test that workspace defaults to main, when nothing is passed as parameter."""
    data = {
        "name": "first project",
        "description": "Project 1",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "one_off",
    }
    response = client.post("/projects/", json=data)
    mock_project_init_db.assert_called_once()
    assert response.status_code == 200
    project = response.json()
    assert project["workspace_slug"] == "main"


@mock.patch("phiphi.pipeline_jobs.projects.init_project_db")
@pytest.mark.freeze_time(CREATED_TIME)
def test_create_project_with_non_existing_workspace(
    mock_project_init_db, recreate_tables, client: TestClient
) -> None:
    """Test create and then get of an project, with a workspace that doesn't exist."""
    data = {
        "name": "first project",
        "description": "Project 1",
        "workspace_slug": "non-existing",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "weekly",
    }
    response = client.post("/projects/", json=data)
    mock_project_init_db.assert_not_called()
    assert response.status_code == 400
    assert response.json() == {"detail": "Workspace not found"}


@pytest.mark.freeze_time(CREATED_TIME)
def test_project_with_latest_job_run(client: TestClient, reseed_tables) -> None:
    """Test that the latest job run is returned."""
    response = client.get("/projects/1")
    assert response.status_code == 200
    project = response.json()
    assert project["last_job_run_completed_at"] == "2024-04-01T12:00:20"
    # The job_run that is completed is not the same as the latest_job_run
    assert project["latest_job_run"]["id"] == 20
    assert project["latest_job_run"]["completed_at"] != project["last_job_run_completed_at"]


@pytest.mark.freeze_time(CREATED_TIME)
def test_project_with_latest_job_run_2(client: TestClient, reseed_tables) -> None:
    """Test that the latest job run is returned."""
    response = client.get("/projects/2")
    assert response.status_code == 200
    project = response.json()
    # This job run is not completed and is the latest
    assert project["last_job_run_completed_at"] is None
    assert project["latest_job_run"]["id"] == 6
    assert project["latest_job_run"]["completed_at"] == project["last_job_run_completed_at"]
