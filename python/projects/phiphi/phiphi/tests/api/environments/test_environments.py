"""Test Environments."""
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.api.environments import crud, models


def test_get_environment_by_unique_id(session: sqlalchemy.orm.Session, reseed_tables) -> None:
    """Test getting an environment by unique id."""
    environment = crud.get_environment_by_unique_id(session, "Phoenix")
    assert environment


def test_delete_environment(
    session: sqlalchemy.orm.Session, reseed_tables, client: TestClient
) -> None:
    """Test deleting an environment."""
    response = client.delete("/environments/1")
    assert response.status_code == 200


CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_get_environment(recreate_tables, client: TestClient) -> None:
    """Test creating and get of an environment."""
    data = {"description": "My environment", "name": "test_env"}
    response = client.post("/environments/", json=data)
    assert response.status_code == 200
    environment = response.json()
    assert environment["description"] == data["description"]
    assert environment["name"] == data["name"]
    assert environment["created_at"] == CREATED_TIME

    response = client.get(f"/environments/{environment['id']}")
    assert response.status_code == 200

    environment = response.json()

    assert environment["description"] == data["description"]
    assert environment["name"] == data["name"]
    assert environment["created_at"] == CREATED_TIME


def test_get_environment_not_found(client: TestClient, recreate_tables) -> None:
    """Test getting an environment that does not exist."""
    response = client.get("/environments/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Environment not found"}


def test_get_environments(client: TestClient, reseed_tables) -> None:
    """Test getting environments."""
    response = client.get("/environments/")
    assert response.status_code == 200
    environments = response.json()
    assert len(environments) == 2


@pytest.mark.freeze_time(UPDATE_TIME)
def test_update_environment(
    client: TestClient, reseed_tables, session: sqlalchemy.orm.Session
) -> None:
    """Test updating an environment."""
    data = {"description": "new_env"}
    environment_id = 1
    response = client.put(f"/environments/{environment_id}", json=data)
    assert response.status_code == 200
    environment = response.json()
    assert environment["description"] == data["description"]
    db_environment = session.get(models.Environment, environment_id)
    assert db_environment
    assert db_environment.description == data["description"]
    assert db_environment.updated_at.isoformat() == UPDATE_TIME


def test_update_environment_not_found(client: TestClient, recreate_tables) -> None:
    """Test updating an environment that does not exist."""
    data = {"description": "new_env"}
    response = client.put("/environments/1", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Environment not found"}


def test_unique_id_different_with_same_name(recreate_tables, client: TestClient) -> None:
    """Test that the unique Id will be different for environments with the same name."""
    data = {"description": "test env", "name": "Test"}
    response = client.post("/environments/", json=data)
    assert response.status_code == 200
    environment_1 = response.json()
    assert environment_1["description"] == data["description"]
    assert environment_1["name"] == data["name"]

    data_2 = {"description": "test env 2", "name": "Test"}
    response = client.post("/environments/", json=data_2)
    assert response.status_code == 200

    environment_2 = response.json()

    assert environment_1["unique_id"] != environment_2["unique_id"]
