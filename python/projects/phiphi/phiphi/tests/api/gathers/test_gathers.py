"""Test Gathers."""
from datetime import datetime
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from prefect.client.schemas import objects

from phiphi.api.projects.gathers import crud
from phiphi.api.projects.job_runs import crud as job_runs_crud
from phiphi.api.projects.job_runs import schemas as job_run_schemas


def test_get_gather_crud(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    gather = crud.get_gather(reseed_tables, 1, 1)
    assert gather
    assert gather.id == 1
    assert gather.project_id == 1
    assert gather.latest_job_run
    assert gather.latest_job_run.id == 5
    assert gather.latest_job_run.status == "awaiting_start"


def test_get_gather(client: TestClient, reseed_tables) -> None:
    """Test getting gather."""
    response = client.get("/projects/1/gathers/1")
    assert response.status_code == 200
    gather_1 = response.json()

    assert gather_1["id"] == 1
    assert gather_1["project_id"] == 1
    assert gather_1["latest_job_run"]["id"] == 5
    assert gather_1["latest_job_run"]["status"] == "awaiting_start"
    # Get of a gather should includes the child properties
    assert gather_1["limit_posts_per_account"] == 1000

    response_2 = client.get("/projects/2/gathers/4")
    assert response_2.status_code == 200
    gather_2 = response_2.json()
    assert gather_1["name"] != gather_2["name"]
    assert gather_2["id"] == 4
    assert gather_2["project_id"] == 2
    # Get of a gather should include the comment child properties
    assert gather_2["limit_comments_per_post"] == 1000


def test_get_gather_2(client: TestClient, reseed_tables) -> None:
    """Test getting gather 2."""
    # Check that it is not always the first gather that is gotten
    response_3 = client.get("/projects/1/gathers/2")
    gather_3 = response_3.json()
    assert gather_3["id"] == 2
    assert gather_3["project_id"] == 1
    assert gather_3["latest_job_run"]["id"] == 4
    assert gather_3["latest_job_run"]["status"] == "completed_sucessfully"
    # Gather 2 has a foreign job type of gather_classify_tabulate
    assert gather_3["latest_job_run"]["foreign_job_type"] == "gather_classify_tabulate"


def test_get_gather_with_no_job_run(client: TestClient, reseed_tables) -> None:
    """Test get gather with no job run."""
    response = client.get("/projects/2/gathers/4")
    gather = response.json()
    assert gather["id"] == 4
    assert gather["project_id"] == 2
    assert gather["latest_job_run"] is None


def test_get_gathers(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/projects/1/gathers/")
    assert response.status_code == 200
    gathers = response.json()
    # Currently this includes even the deleted gathers
    assert len(gathers) == 3

    response = client.get("/projects/2/gathers/")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 5


def test_get_gathers_estimate(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/projects/1/gathers/1/estimate")
    assert response.status_code == 200
    gather = response.json()
    assert gather["id"] == 1
    assert gather["estimated_credit_cost"] == 0
    assert gather["estimated_duration_minutes"] == 0


DELETED_TIME = "2024-04-01T12:00:01"


@pytest.mark.freeze_time(DELETED_TIME)
@mock.patch("phiphi.api.projects.job_runs.prefect_deployment.wrapped_run_deployment")
def test_delete_gather(m_run_deployment, reseed_tables, client: TestClient, session) -> None:
    """Test deleting a gather."""
    # Need to add attributes to the mock object to avoid errors
    mock_flow_run = mock.MagicMock(spec=objects.FlowRun)
    mock_flow_run.id = "mock_uuid"
    mock_flow_run.name = "mock_flow_run"
    m_run_deployment.return_value = mock_flow_run
    response = client.delete("/projects/1/gathers/1")
    assert response.status_code == 200
    gather = response.json()
    assert gather["id"] == 1
    assert gather["project_id"] == 1
    assert gather["delete_job_run"] is not None
    assert gather["delete_job_run"]["status"] == "in_queue"
    assert gather["delete_job_run"]["created_at"] == DELETED_TIME
    m_run_deployment.assert_called_once_with(
        name="flow_runner_flow/flow_runner_flow",
        parameters={
            "project_id": 1,
            "job_type": job_run_schemas.ForeignJobType.delete_gather_tabulate,
            "job_source_id": 1,
            "job_run_id": gather["delete_job_run"]["id"],
        },
    )
    # Because we need to get the status of the delete_job_run we don't filter for deleted gathers
    # on a GET.
    response = client.get("/projects/1/gathers/1")
    assert response.status_code == 200
    gather_2 = response.json()
    assert gather["id"] == gather_2["id"]
    assert gather["project_id"] == gather_2["project_id"]
    assert gather["delete_job_run"] == gather_2["delete_job_run"]
    # Test that a second delete job run is called on a deleted gather will return 400 as you can't
    # have two job runs at the same time.
    m_run_deployment.reset_mock()
    response = client.delete("/projects/1/gathers/1")
    assert response.status_code == 400
    m_run_deployment.assert_not_called()

    job_runs_crud.update_job_run(
        session,
        job_run_data=job_run_schemas.JobRunUpdateCompleted(
            id=gather["delete_job_run"]["id"],
            status=job_run_schemas.Status.completed_sucessfully,
            completed_at=datetime.strptime(DELETED_TIME, "%Y-%m-%dT%H:%M:%S"),
        ),
    )

    # Test that a second delete job run is called on a deleted gather when the delete job run is
    # complete will run
    # This is so that if the delete job run fails we can try again.
    m_run_deployment.reset_mock()
    response = client.delete("/projects/1/gathers/1")
    assert response.status_code == 200
    gather = response.json()
    assert gather["id"] == 1
    assert gather["project_id"] == 1
    assert gather["delete_job_run"] is not None
    assert gather["delete_job_run"]["status"] == "in_queue"
    assert gather["delete_job_run"]["created_at"] == DELETED_TIME
    m_run_deployment.assert_called_with(
        name="flow_runner_flow/flow_runner_flow",
        parameters={
            "project_id": 1,
            "job_type": job_run_schemas.ForeignJobType.delete_gather_tabulate,
            "job_source_id": 1,
            "job_run_id": gather["delete_job_run"]["id"],
        },
    )
