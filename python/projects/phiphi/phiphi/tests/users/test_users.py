"""Test Users."""
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.users import models


def test_user(session: sqlalchemy.orm.Session, recreate_tables) -> None:
    """Test that there are no users."""
    response = session.execute(sqlalchemy.select(sqlalchemy.func.count()).select_from(models.User))
    count = response.one()
    assert count
    assert count[0] == 0


def test_user_seeded(session: sqlalchemy.orm.Session, reseed_tables) -> None:
    """Test that the database is seeded."""
    response = session.execute(sqlalchemy.select(sqlalchemy.func.count()).select_from(models.User))
    count = response.one()
    assert count
    assert count[0] == 3


CREATED_TIME = "2024-01-01T12:00:01"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_read_user(recreate_tables, client: TestClient) -> None:
    """Test creating a user."""
    data = {"email": "test@test.com", "display_name": "test"}
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == data["email"]
    assert user["display_name"] == data["display_name"]
    assert user["created_at"] == CREATED_TIME

    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200

    user = response.json()

    assert user["email"] == data["email"]
    assert user["display_name"] == data["display_name"]
    assert user["created_at"] == CREATED_TIME


def test_read_user_not_found(client: TestClient, recreate_tables) -> None:
    """Test reading a user that does not exist."""
    response = client.get("/users/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_users(client: TestClient, reseed_tables) -> None:
    """Test reading users."""
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 3


def test_read_users_pagination(client: TestClient, reseed_tables) -> None:
    """Test reading users with pagination."""
    response = client.get("/users/?start=1&end=1")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["id"] == 2
