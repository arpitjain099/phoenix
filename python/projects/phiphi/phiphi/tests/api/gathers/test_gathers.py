"""Test Gathers."""
from fastapi.testclient import TestClient

from phiphi.api.projects.gathers import crud


def test_get_gather_crud(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    gather = crud.get_gather(reseed_tables, 1, 1)
    assert gather
    assert gather.id == 1
    assert gather.project_id == 1
    assert gather.latest_job_run
    assert gather.latest_job_run.id == 4
    assert gather.latest_job_run.status == "awaiting_start"


def test_get_gather(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/projects/1/gathers/1")
    assert response.status_code == 200
    gather_1 = response.json()

    assert gather_1["id"] == 1
    assert gather_1["project_id"] == 1
    assert gather_1["latest_job_run"]["id"] == 4
    assert gather_1["latest_job_run"]["status"] == "awaiting_start"

    response_2 = client.get("/projects/2/gathers/3")
    assert response_2.status_code == 200
    gather_2 = response_2.json()
    assert gather_1["description"] != gather_2["description"]

    assert gather_1["id"] == 1
    assert gather_1["project_id"] == 1
    assert gather_2["id"] == 3
    assert gather_2["project_id"] == 2

    # Check that it is not always the first gather that is gotten
    response_3 = client.get("/projects/1/gathers/2")
    gather_3 = response_3.json()
    assert gather_3["id"] == 2
    assert gather_3["project_id"] == 1


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
    assert len(gathers) == 3

    response = client.get("/projects/2/gathers/")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 3


def test_get_gathers_estimate(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/projects/1/gathers/1/estimate")
    assert response.status_code == 200
    gather = response.json()
    assert gather["id"] == 1
    assert gather["estimated_credit_cost"] == 0
    assert gather["estimated_duration_minutes"] == 0
