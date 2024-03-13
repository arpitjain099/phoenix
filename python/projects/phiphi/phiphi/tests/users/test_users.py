"""Test Users."""
import sqlalchemy
from fastapi.testclient import TestClient

from phiphi.users import models


def test_user(session: sqlalchemy.orm.Session) -> None:
    """Test that there are no users."""
    response = session.execute(sqlalchemy.select(sqlalchemy.func.count()).select_from(models.User))
    count = response.one()
    assert count
    assert count[0] == 0


def test_create_user(recreate_tables, client: TestClient) -> None:
    """Test creating a user."""
    data = {"email": "test@test.com", "display_name": "test"}
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == data["email"]
    assert user["display_name"] == data["display_name"]
