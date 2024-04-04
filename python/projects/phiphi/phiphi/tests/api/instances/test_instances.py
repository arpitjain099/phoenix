"""Test Instances."""
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.api.instances import models


def test_instance_seeded(session: sqlalchemy.orm.Session, reseed_tables) -> None:
    """Test that the database is seeded."""
    response = session.execute(
        sqlalchemy.select(sqlalchemy.func.count()).select_from(models.Instance)
    )
    count = response.one()
    assert count
    assert count[0] == 2


CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_instance(recreate_tables, client: TestClient) -> None:
    """Test create and then get of an instance."""
    data = {
        "name": "first instance",
        "description": "Instance 1",
        "environment_id": "main",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "weekly",
    }
    response = client.post("/instances/", json=data)
    assert response.status_code == 200
    instance = response.json()
    assert instance["name"] == data["name"]
    assert instance["description"] == data["description"]
    assert instance["environment_id"] == data["environment_id"]
    assert instance["pi_deleted_after_days"] == data["pi_deleted_after_days"]
    assert instance["delete_after_days"] == data["delete_after_days"]
    assert instance["expected_usage"] == data["expected_usage"]
    assert instance["created_at"] == CREATED_TIME

    response = client.get(f"/instances/{instance['id']}")
    assert response.status_code == 200

    instance = response.json()

    assert instance["name"] == data["name"]
    assert instance["description"] == data["description"]
    assert instance["created_at"] == CREATED_TIME
    assert instance["environment_id"] == data["environment_id"]
    assert instance["pi_deleted_after_days"] == data["pi_deleted_after_days"]
    assert instance["delete_after_days"] == data["delete_after_days"]


def test_get_instance_not_found(client: TestClient, recreate_tables) -> None:
    """Test getting an instance that does not exist."""
    response = client.get("/instances/5")
    assert response.status_code == 404
    assert response.json() == {"detail": "Instance not found"}


def test_get_instances(client: TestClient, reseed_tables) -> None:
    """Test getting instances."""
    response = client.get("/instances/")
    assert response.status_code == 200
    instances = response.json()
    assert len(instances) == 2


def test_get_instances_pagination(client: TestClient, reseed_tables) -> None:
    """Test getting users with pagination."""
    response = client.get("/instances/?start=1&end=1")
    assert response.status_code == 200
    instances = response.json()
    assert len(instances) == 1
    assert instances[0]["id"] == 2


@pytest.mark.freeze_time(UPDATE_TIME)
def test_update_instance(
    client: TestClient, reseed_tables, session: sqlalchemy.orm.Session
) -> None:
    """Test updating an instance."""
    data = {"description": "New instance"}
    instance_id = 1
    response = client.put(f"/instances/{instance_id}", json=data)
    assert response.status_code == 200
    instance = response.json()
    assert instance["description"] == data["description"]
    db_instance = session.get(models.Instance, instance_id)
    assert db_instance
    assert db_instance.description == data["description"]
    assert db_instance.updated_at.isoformat() == UPDATE_TIME


def test_update_instance_not_found(client: TestClient, recreate_tables) -> None:
    """Test updating an instance that does not exist."""
    data = {"description": "New instance"}
    response = client.put("/instances/100", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Instance not found"}


def test_environment_defaults_main(client: TestClient, recreate_tables) -> None:
    """Test that environment defaults to main, when nothing is passed as parameter."""
    data = {
        "name": "first instance",
        "description": "Instance 1",
        "pi_deleted_after_days": 90,
        "delete_after_days": 20,
        "expected_usage": "one_off",
    }
    response = client.post("/instances/", json=data)
    assert response.status_code == 200
    instance = response.json()
    assert instance["environment_id"] == "main"
