"""Test Gathers."""
import pytest
from fastapi.testclient import TestClient

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


def test_get_apify_gathers(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/instances/1/gathers/apify")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 2


def test_get_apify_gather(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/instances/1/gathers/apify/1")
    assert response.status_code == 200
    gather_1 = response.json()

    response_2 = client.get("/instances/2/gathers/apify/3")
    assert response_2.status_code == 200
    gather_2 = response_2.json()
    assert gather_1["description"] != gather_2["description"]
    assert gather_1["input"] != gather_2["input"]
    assert gather_1["start_date"] != gather_2["start_date"]
    assert gather_1["end_date"] != gather_2["end_date"]
    assert gather_1["limit_messages"] != gather_2["limit_messages"]
    assert gather_1["limit_replies"] != gather_2["limit_replies"]

    assert gather_1["id"] == 1
    assert gather_1["instance_id"] == 1
    assert gather_2["id"] == 3
    assert gather_2["instance_id"] == 2

    # Check that it is not always the first gather that is gotten
    response_3 = client.get("/instances/1/gathers/apify/2")
    gather_3 = response_3.json()
    assert gather_3["id"] == 2
    assert gather_3["instance_id"] == 1


def test_get_gathers(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    response = client.get("/instances/1/gathers/")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 2

    response = client.get("/instances/2/gathers/")
    assert response.status_code == 200
    gathers = response.json()
    assert len(gathers) == 1


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_apify_gather(reseed_tables, client: TestClient) -> None:
    """Test create and then get of a gather."""
    data = {
        "description": "First apify gather",
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
    response = client.post("/instances/1/gathers/apify", json=data)
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

    response = client.get(f"/instances/1/gathers/apify/{gather['id']}")
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
