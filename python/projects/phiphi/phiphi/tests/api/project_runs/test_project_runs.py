"""Test Project Runs."""
import datetime

import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.api.projects.project_runs import crud, schemas

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_project_runs(reseed_tables, client: TestClient) -> None:
    """Test create and then get of an project run."""
    response = client.post("/projects/1/runs/")
    assert response.status_code == 200
    project_runs = response.json()

    response = client.get(f"/projects/{project_runs['project_id']}/runs/last")
    assert response.status_code == 200

    project = response.json()

    assert project["environment_slug"] == project_runs["environment_slug"]
    assert project_runs["created_at"] == CREATED_TIME


def test_get_project_runs(client: TestClient, reseed_tables) -> None:
    """Test getting project runs."""
    response = client.get("/projects/1/runs/")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 1


def test_completed_run_status(
    session: sqlalchemy.orm.Session, reseed_tables, client: TestClient
) -> None:
    """Test completed run status."""
    response = crud.update_project_runs(
        session, 1, schemas.ProjectRunsUpdate(completed_at=datetime.datetime.now())
    )
    assert response
    assert response.run_status == "completed"


def test_failed_run_status(
    session: sqlalchemy.orm.Session, reseed_tables, client: TestClient
) -> None:
    """Test failed run status."""
    response = crud.update_project_runs(
        session, 2, schemas.ProjectRunsUpdate(failed_at=datetime.datetime.now())
    )
    assert response
    assert response.run_status == "failed"


def test_processing_run_status(
    session: sqlalchemy.orm.Session, reseed_tables, client: TestClient
) -> None:
    """Test prorcessing run status."""
    response = crud.update_project_runs(
        session, 1, schemas.ProjectRunsUpdate(started_processing_at=datetime.datetime.now())
    )
    assert response
    assert response.run_status == "processing"


def test_in_queue_run_status(reseed_tables, client: TestClient) -> None:
    """Test in_queue run status."""
    response = client.get("/projects/1/runs/?run_status=in_queue")
    assert response.status_code == 200
    project = response.json()

    assert project[0]["run_status"] == "in_queue"
