"""Test Gathers."""
import pytest
from fastapi.testclient import TestClient

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


def test_get_apify_gathers(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/gathers/apify")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 2


def test_get_gathers(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/gathers/")
    assert response.status_code == 200


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_apify_gather(recreate_tables, client: TestClient) -> None:
    """Test create and then get of a gather."""
    data = {
        "description": "Firt apify gather",
        "instance_id": 1,
        "input": {"type": "author_url_list", "data": ["Author_1"]},
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
    assert gather["input"] == data["input"]
    assert gather["instance_id"] == data["instance_id"]
    assert gather["start_date"] == data["start_date"]
    assert gather["end_date"] == data["end_date"]
    assert gather["limit_messages"] == data["limit_messages"]
    assert gather["limit_replies"] == data["limit_replies"]
    assert gather["created_at"] == CREATED_TIME

    response = client.get(f"/gathers/apify/{gather['id']}")
    assert response.status_code == 200

    gather = response.json()

    assert gather["description"] == data["description"]
    assert gather["input"] == data["input"]
    assert gather["instance_id"] == data["instance_id"]
    assert gather["start_date"] == data["start_date"]
    assert gather["end_date"] == data["end_date"]
    assert gather["limit_messages"] == data["limit_messages"]
    assert gather["limit_replies"] == data["limit_replies"]
    assert gather["created_at"] == CREATED_TIME
