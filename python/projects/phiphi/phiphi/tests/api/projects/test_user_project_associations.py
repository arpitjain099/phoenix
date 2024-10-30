"""Test user project associations."""
import sqlalchemy as sa
from fastapi.testclient import TestClient


def test_user_project_associations_create(
    reseed_tables: sa.orm.Session, client: TestClient
) -> None:
    """Test creating a user project association."""
    data = {"role": "user"}
    response = client.post("/projects/1/users/3", json=data)
    assert response.status_code == 200
    association = response.json()
    assert association["user_id"] == 3
    assert association["project_id"] == 1
    assert association["role"] == "user"


def test_user_project_associations_create_duplicate(
    reseed_tables: sa.orm.Session, client: TestClient
) -> None:
    """Test creating a user project association that is duplicate."""
    data = {"role": "user"}
    response = client.post("/projects/1/users/2", json=data)
    assert response.status_code == 400
    json = response.json()
    assert json == {"detail": "User project association already exists"}
