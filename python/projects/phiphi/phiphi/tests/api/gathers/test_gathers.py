"""Test Gathers."""
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.api.gathers import models

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


def test_get_apify_gathers(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/gathers/apify")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 2


@pytest.mark.freeze_time(UPDATE_TIME)
def test_update_apify_gather(
    client: TestClient, reseed_tables, session: sqlalchemy.orm.Session
) -> None:
    """Test updating a gather."""
    data = {"mark_to_delete": True}
    gather_id = 1
    response = client.put(f"/gathers/apify/{gather_id}", json=data)
    assert response.status_code == 200
    gather = response.json()
    assert gather["mark_to_delete"] == data["mark_to_delete"]
    db_gather = session.get(models.Gather, gather_id)
    assert db_gather
    assert db_gather.mark_to_delete == data["mark_to_delete"]
    assert db_gather.updated_at.isoformat() == UPDATE_TIME


def test_update_gather_not_found(client: TestClient, recreate_tables) -> None:
    """Test updating a gather that does not exist."""
    data = {"mark_to_delete": True}
    response = client.put("/gathers/apify/100", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Gather not found"}


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_apify_gather(recreate_tables, client: TestClient) -> None:
    """Test create and then get of a gather."""
    data = {
        "description": "Firt apify gather",
        "instance_id": 1,
        "input_type": "author_url_list",
        "input_data": "lorem ipsum",
        "platform": "facebook",
        "data_type": "messages",
        "start_date": "2024-04-08T08:41:05",
        "end_date": "2024-04-08T08:41:05",
        "limit_messages": 1000,
        "limit_replies": 100,
        "nested_replies": False,
    }
    response = client.post("/gathers/apify", json=data)
    assert response.status_code == 200
    gather = response.json()
    assert gather["description"] == data["description"]
    assert gather["input_type"] == data["input_type"]
    assert gather["instance_id"] == data["instance_id"]
    assert gather["input_data"] == data["input_data"]
    assert gather["start_date"] == data["start_date"]
    assert gather["end_date"] == data["end_date"]
    assert gather["limit_messages"] == data["limit_messages"]
    assert gather["limit_replies"] == data["limit_replies"]
    assert gather["created_at"] == CREATED_TIME

    response = client.get(f"/gathers/apify/{gather['id']}")
    assert response.status_code == 200

    gather = response.json()

    assert gather["description"] == data["description"]
    assert gather["input_type"] == data["input_type"]
    assert gather["instance_id"] == data["instance_id"]
    assert gather["input_data"] == data["input_data"]
    assert gather["start_date"] == data["start_date"]
    assert gather["end_date"] == data["end_date"]
    assert gather["limit_messages"] == data["limit_messages"]
    assert gather["limit_replies"] == data["limit_replies"]
    assert gather["created_at"] == CREATED_TIME
