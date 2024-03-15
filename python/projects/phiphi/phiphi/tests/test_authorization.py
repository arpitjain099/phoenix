"""Authorization test."""
from fastapi.testclient import TestClient

from phiphi.core import config


def test_read_me_no_header(client: TestClient, reseed_tables) -> None:
    """Test authorization users/me with no header."""
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Cannot authenticate."}


def test_read_me_first_admin(client_first_admin_user: TestClient, reseed_tables) -> None:
    """Test authorization users/me with header for admin."""
    response = client_first_admin_user.get("/users/me")
    assert response.status_code == 200
    user = response.json()

    assert user["email"] == config.settings.FIRST_ADMIN_USER_EMAIL
    assert user["display_name"] == config.settings.FIRST_ADMIN_USER_DISPLAY_NAME
