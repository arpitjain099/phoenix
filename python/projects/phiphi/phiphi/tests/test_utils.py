"""Test utils."""
import pytest

from phiphi import utils

MAIN_APIFY_API_KEY = "main_apify_key"
OTHER_APIFY_API_KEY = "other_apify_key"
OTHER_ENV_SLUG = "other_env_slug"
APIFY_API_KEYS_STR_1 = (
    f'{{"main_env_slug": "{MAIN_APIFY_API_KEY}", "{OTHER_ENV_SLUG}": "{OTHER_APIFY_API_KEY}"}}'
)
SETTINGS_ENV_MAIN = {
    "APIFY_API_KEYS": APIFY_API_KEYS_STR_1,
    "FIRST_ENVIRONMENT_SLUG": "main_env_slug",
}
SETTINGS_ENV_OTHER = {
    "APIFY_API_KEYS": APIFY_API_KEYS_STR_1,
    "FIRST_ENVIRONMENT_SLUG": OTHER_ENV_SLUG,
}


@pytest.mark.patch_settings(SETTINGS_ENV_MAIN)
def test_get_apify_keys_main(patch_settings):
    """Test get apify keys."""
    assert utils.get_apify_api_key() == MAIN_APIFY_API_KEY


@pytest.mark.patch_settings(SETTINGS_ENV_MAIN)
def test_get_apify_keys_other(patch_settings):
    """Test get apify keys for other env."""
    assert utils.get_apify_api_key(OTHER_ENV_SLUG) == OTHER_APIFY_API_KEY


@pytest.mark.patch_settings(SETTINGS_ENV_OTHER)
def test_get_apify_keys_other_env(patch_settings):
    """Test get apify keys."""
    assert utils.get_apify_api_key() == OTHER_APIFY_API_KEY


@pytest.mark.patch_settings(SETTINGS_ENV_MAIN)
def test_get_apify_keys_not_found(patch_settings):
    """Test get apify keys."""
    with pytest.raises(ValueError):
        utils.get_apify_api_key("not_found")


@pytest.mark.patch_settings(
    {"APIFY_API_KEYS": APIFY_API_KEYS_STR_1, "FIRST_ENVIRONMENT_SLUG": "not_found"}
)
def test_get_apify_keys_not_found_env(patch_settings):
    """Test get apify keys."""
    with pytest.raises(ValueError):
        utils.get_apify_api_key()


def test_get_project_namespace():
    """Test get project namespace."""
    assert utils.get_project_namespace(1) == "project_id1"


def test_get_project_namespace_prefix():
    """Test get project namespace."""
    assert utils.get_project_namespace(1, "test_") == "test_project_id1"
