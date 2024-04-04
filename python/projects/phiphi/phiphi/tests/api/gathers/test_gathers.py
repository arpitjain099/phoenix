"""Test Gathers."""
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.api.gathers import models

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


def test_get_gathers(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/gathers/")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 2


@pytest.mark.freeze_time(UPDATE_TIME)
def test_update_gather(client: TestClient, reseed_tables, session: sqlalchemy.orm.Session) -> None:
    """Test updating a gather."""
    data = {"description": "New gather"}
    gather_id = 1
    response = client.put(f"/gathers/{gather_id}", json=data)
    assert response.status_code == 200
    gather = response.json()
    assert gather["description"] == data["description"]
    db_gather = session.get(models.Gather, gather_id)
    assert db_gather
    assert db_gather.description == data["description"]
    assert db_gather.updated_at.isoformat() == UPDATE_TIME


def test_update_gather_not_found(client: TestClient, recreate_tables) -> None:
    """Test updating a gather that does not exist."""
    data = {"description": "New gather"}
    response = client.put("/gathers/100", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Instance not found"}


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_gather(recreate_tables, client: TestClient) -> None:
    """Test create and then get of a gather."""
    data = {
        "description": "Phoenix gather",
        "config_type": "apify_facebook_messages",
        "config": {
            "start_date": CREATED_TIME,
            "end_date": UPDATE_TIME,
            "limit_messages": 1000,
            "limit_replies": 100,
            "nested_replies": False,
            "config_input": "author_url_list",
        },
    }
    response = client.post("/gathers/", json=data)
    assert response.status_code == 200
    gather = response.json()
    assert gather["description"] == data["description"]
    assert gather["config_type"] == data["config_type"]
    assert gather["config"] == data["config"]
    assert gather["created_at"] == CREATED_TIME

    response = client.get(f"/gathers/{gather['id']}")
    assert response.status_code == 200

    gather = response.json()

    assert gather["description"] == data["description"]
    assert gather["created_at"] == CREATED_TIME
    assert gather["config_type"] == data["config_type"]
    assert gather["config"] == data["config"]
