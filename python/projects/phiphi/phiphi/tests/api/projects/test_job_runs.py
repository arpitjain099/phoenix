"""Test job runs routes."""
import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects.job_runs import schemas

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_job_runs(reseed_tables, client: TestClient) -> None:
    """Test create and then get of an job run."""
    data = {
        "foreign_id": 1,
        "foreign_job_type": "gather",
    }

    response = client.post("/projects/1/job_runs/", json=data)
    assert response.status_code == 200
    job_run = response.json()
    assert job_run["foreign_id"] == data["foreign_id"]
    assert job_run["foreign_job_type"] == data["foreign_job_type"]
    assert job_run["created_at"] == CREATED_TIME
    assert job_run["project_id"] == 1
    assert job_run["status"] == schemas.Status.awaiting_start

    response = client.get(f"/projects/1/job_runs/{job_run['id']}")
    assert response.status_code == 200

    job_run = response.json()
    assert job_run["id"] == job_run["id"]


def test_get_job_runs(client: TestClient, reseed_tables) -> None:
    """Test getting job runs."""
    response = client.get("/projects/1/job_runs/")
    assert response.status_code == 200
    job_runs = response.json()
    assert len(job_runs) == 2
    # Assert desc id
    assert job_runs[0]["id"] == 2
    assert job_runs[1]["id"] == 1

    response = client.get("/projects/2/job_runs/")
    assert response.status_code == 200
    job_runs = response.json()
    assert len(job_runs) == 1
    assert job_runs[0]["id"] == 3


def test_get_job_runs_pagination(client: TestClient, reseed_tables) -> None:
    """Test getting job runs with pagination."""
    response = client.get("/projects/1/job_runs/?start=0&end=1")
    assert response.status_code == 200
    job_runs = response.json()
    assert len(job_runs) == 1
