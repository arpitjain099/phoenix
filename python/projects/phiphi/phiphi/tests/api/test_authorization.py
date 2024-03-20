"""Authorization test."""
import pytest
from fastapi.testclient import TestClient

from phiphi import config


# Making sure that the settings are not using cookie auth so is consistent with a production env
@pytest.mark.patch_settings({"USE_COOKIE_AUTH": False})
def test_read_me_no_header(client: TestClient, reseed_tables, patch_settings) -> None:
    """Test authorization users/me with no header."""
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Cannot authenticate."}


# Making sure that the settings are not using cookie auth so is consistent with a production env
@pytest.mark.patch_settings({"USE_COOKIE_AUTH": False})
def test_read_me_first_admin(
    client_first_admin_user: TestClient, reseed_tables, patch_settings
) -> None:
    """Test authorization users/me with header for admin."""
    response = client_first_admin_user.get("/users/me")
    assert response.status_code == 200
    user = response.json()

    assert user["email"] == config.settings.FIRST_ADMIN_USER_EMAIL
    assert user["display_name"] == config.settings.FIRST_ADMIN_USER_DISPLAY_NAME
