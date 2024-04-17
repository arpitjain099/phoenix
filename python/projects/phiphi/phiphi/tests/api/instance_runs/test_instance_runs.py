"""Test Instance Runs."""
import pytest
from fastapi.testclient import TestClient

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_instance_runs(reseed_tables, client: TestClient) -> None:
    """Test create and then get of an instance run."""
    response = client.post("/instances/1/runs/")
    assert response.status_code == 200
    instance_runs = response.json()

    response = client.get(f"/instances/{instance_runs['instance_id']}/runs/last")
    assert response.status_code == 200

    instance = response.json()

    assert instance["environment_slug"] == instance_runs["environment_slug"]
    assert instance_runs["created_at"] == CREATED_TIME


def test_get_instance_runs(client: TestClient, reseed_tables) -> None:
    """Test getting instance runs."""
    response = client.get("/instances/1/runs/")
    assert response.status_code == 200
    instances = response.json()
    assert len(instances) == 1


def test_completed_run_status(reseed_tables, client: TestClient) -> None:
    """Test completed run status."""
    data = {"completed_at": CREATED_TIME}
    response = client.put("/instances/runs/1/", json=data)
    assert response.status_code == 200
    instance = response.json()

    assert instance["run_status"] == "completed"


def test_failed_run_status(reseed_tables, client: TestClient) -> None:
    """Test completed run status."""
    data = {"failed_at": CREATED_TIME}
    response = client.put("/instances/runs/2/", json=data)
    assert response.status_code == 200
    instance = response.json()

    assert instance["run_status"] == "failed"


def test_processing_run_status(reseed_tables, client: TestClient) -> None:
    """Test completed run status."""
    data = {"started_processing_at": CREATED_TIME}
    response = client.put("/instances/runs/1/", json=data)
    assert response.status_code == 200
    instance = response.json()

    assert instance["run_status"] == "processing"
