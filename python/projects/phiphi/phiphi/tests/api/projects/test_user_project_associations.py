"""Test user project associations."""
import sqlalchemy as sa
from fastapi.testclient import TestClient


def test_user_project_associations_create(
    reseed_tables: sa.orm.Session, client_admin: TestClient
) -> None:
    """Test creating a user project association."""
    data = {"role": "user"}
    response = client_admin.post("/projects/1/users/3", json=data)
    assert response.status_code == 200
    association = response.json()
    assert association["user_id"] == 3
    assert association["project_id"] == 1
    assert association["role"] == "user"


def test_user_project_associations_create_duplicate(
    reseed_tables: sa.orm.Session, client_admin: TestClient
) -> None:
    """Test creating a user project association that is duplicate."""
    data = {"role": "user"}
    response = client_admin.post("/projects/1/users/2", json=data)
    assert response.status_code == 400
    json = response.json()
    assert json == {"detail": "User project association already exists"}


def test_user_project_associations_delete(
    reseed_tables: sa.orm.Session, client_admin: TestClient
) -> None:
    """Test deleting a user project association."""
    response = client_admin.delete("/projects/1/users/2")
    assert response.status_code == 200


def test_user_project_associations_delete_not_found(
    reseed_tables: sa.orm.Session, client_admin: TestClient
) -> None:
    """Test deleting a user project association."""
    response = client_admin.delete("/projects/1/users/3")
    assert response.status_code == 404
    json = response.json()
    assert json == {"detail": "User project association not found"}
