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
