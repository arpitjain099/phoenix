"""Test job runs routes."""
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from prefect.client.schemas import objects

from phiphi.api.projects.job_runs import schemas

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
@mock.patch("phiphi.api.projects.job_runs.prefect_deployment.wrapped_run_deployment")
def test_create_get_job_runs(m_run_deployment, reseed_tables, client: TestClient) -> None:
    """Test create and then get of an job run."""
    data = {
        "foreign_id": 4,
        "foreign_job_type": "gather",
    }

    project_id = 2

    mock_flow_run = mock.MagicMock(spec=objects.FlowRun)
    mock_flow_run.id = "mock_uuid"
    mock_flow_run.name = "mock_flow_run"
    m_run_deployment.return_value = mock_flow_run

    response = client.post(f"/projects/{project_id}/job_runs/", json=data)
    assert response.status_code == 200
    job_run = response.json()
    assert job_run["foreign_id"] == data["foreign_id"]
    assert job_run["foreign_job_type"] == data["foreign_job_type"]
    assert job_run["created_at"] == CREATED_TIME
    assert job_run["project_id"] == project_id
    assert job_run["status"] == schemas.Status.in_queue
    assert job_run["flow_run_id"] == "mock_uuid"
    assert job_run["flow_run_name"] == "mock_flow_run"
    assert job_run["completed_at"] is None
    m_run_deployment.assert_called_once_with(
        name="flow_runner_flow/flow_runner_flow",
        parameters={
            "project_id": project_id,
            "job_type": data["foreign_job_type"],
            "job_source_id": data["foreign_id"],
            "job_run_id": job_run["id"],
        },
    )

    response = client.get(f"/projects/{project_id}/job_runs/{job_run['id']}")
    assert response.status_code == 200

    job_run = response.json()
    assert job_run["id"] == job_run["id"]


@pytest.mark.freeze_time(CREATED_TIME)
@mock.patch("phiphi.api.projects.job_runs.prefect_deployment.wrapped_run_deployment")
def test_create_run_deployments_error(m_run_deployment, reseed_tables, client: TestClient) -> None:
    """Test that if an error occurs in the deployment, the job run is updated."""
    data = {
        "foreign_id": 4,
        "foreign_job_type": "gather",
    }

    project_id = 2

    m_run_deployment.side_effect = Exception("Error")

    response = client.post(f"/projects/{project_id}/job_runs/", json=data)
    assert response.status_code == 200
    job_run = response.json()
    assert job_run["foreign_id"] == data["foreign_id"]
    assert job_run["foreign_job_type"] == data["foreign_job_type"]
    assert job_run["created_at"] == CREATED_TIME
    assert job_run["project_id"] == project_id
    assert job_run["status"] == schemas.Status.failed
    assert job_run["completed_at"] == CREATED_TIME

    response = client.get(f"/projects/{project_id}/job_runs/{job_run['id']}")
    assert response.status_code == 200

    job_run = response.json()
    assert job_run["id"] == job_run["id"]
    assert job_run["status"] == schemas.Status.failed

    # Second call to get the job run now works as the first job is completed
    mock_flow_run = mock.MagicMock(spec=objects.FlowRun)
    mock_flow_run.id = "mock_uuid"
    mock_flow_run.name = "mock_flow_run"
    m_run_deployment.return_value = mock_flow_run
    m_run_deployment.side_effect = None
    response = client.post(f"/projects/{project_id}/job_runs/", json=data)
    assert response.status_code == 200
    job_run_2 = response.json()
    assert job_run_2["foreign_id"] == data["foreign_id"]
    assert job_run_2["foreign_job_type"] == data["foreign_job_type"]
    assert job_run_2["created_at"] == CREATED_TIME
    assert job_run_2["project_id"] == project_id
    assert job_run_2["status"] == schemas.Status.in_queue
    assert job_run_2["flow_run_id"] == "mock_uuid"
    assert job_run_2["flow_run_name"] == "mock_flow_run"
    assert job_run_2["id"] != job_run["id"]


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_guard_for_repeated_job_run(reseed_tables, client: TestClient) -> None:
    """Test don't allow to create a second running job."""
    data = {
        "foreign_id": 1,
        "foreign_job_type": "gather",
    }

    response = client.post("/projects/1/job_runs/", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Foreign object has an active job run. Type: ForeignJobType.gather, Id: 1"
    }


def test_create_guard(reseed_tables, client: TestClient) -> None:
    """Test that if a gather is not found, a job run is not created."""
    data = {
        "foreign_id": 5,
        "foreign_job_type": "gather",
    }

    # Project is not found
    response = client.post("/projects/4/job_runs/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Project not found"}

    # Project is found and gather exists but the gather is not in the project
    data = {
        "foreign_id": 3,
        "foreign_job_type": "gather",
    }
    response = client.post("/projects/1/job_runs/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Gather not found"}


def test_create_guard_tabulate(reseed_tables, client: TestClient) -> None:
    """Test that if tabulate is not 0."""
    data = {
        "foreign_id": 1,
        "foreign_job_type": "tabulate",
    }

    # Project is not found
    response = client.post("/projects/4/job_runs/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Tabulate must have a foreign_id of 0"}

    # Project is found and gather exists but the gather is not in the project
    data = {
        "foreign_id": 3,
        "foreign_job_type": "gather",
    }
    response = client.post("/projects/1/job_runs/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Gather not found"}


def test_get_job_runs(client: TestClient, reseed_tables) -> None:
    """Test getting job runs."""
    response = client.get("/projects/1/job_runs/")
    assert response.status_code == 200
    job_runs = response.json()
    assert len(job_runs) == 7
    # Assert desc id
    assert job_runs[0]["id"] == 8
    assert job_runs[5]["id"] == 2

    response = client.get("/projects/2/job_runs/")
    assert response.status_code == 200
    job_runs = response.json()
    assert len(job_runs) == 1
    assert job_runs[0]["id"] == 6


def test_get_job_runs_by_type(client: TestClient, reseed_tables) -> None:
    """Test getting job runs."""
    response = client.get("/projects/1/job_runs/?foreign_job_type=gather")
    assert response.status_code == 200
    job_runs = response.json()
    assert len(job_runs) == 3
    # Assert desc id
    assert job_runs[1]["id"] == 2
    assert job_runs[1]["foreign_job_type"] == "gather"
    assert job_runs[2]["id"] == 1
    assert job_runs[2]["foreign_job_type"] == "gather"


def test_get_job_runs_pagination(client: TestClient, reseed_tables) -> None:
    """Test getting job runs with pagination."""
    response = client.get("/projects/1/job_runs/?start=0&end=1")
    assert response.status_code == 200
    job_runs = response.json()
    assert len(job_runs) == 1
