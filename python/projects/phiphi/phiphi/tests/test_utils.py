"""Test utils."""
import pytest

from phiphi import utils

MAIN_APIFY_API_KEY = "main_apify_key"
OTHER_APIFY_API_KEY = "other_apify_key"
OTHER_WORKSPACE_SLUG = "other_workspace_slug"
APIFY_API_KEYS_STR_1 = f'{{"main_workspace_slug": "{MAIN_APIFY_API_KEY}", "{OTHER_WORKSPACE_SLUG}": "{OTHER_APIFY_API_KEY}"}}'  # noqa: E501
SETTINGS_WORKSPACE_MAIN = {
    "APIFY_API_KEYS": APIFY_API_KEYS_STR_1,
    "FIRST_WORKSPACE_SLUG": "main_workspace_slug",
}
SETTINGS_WORKSPACE_OTHER = {
    "APIFY_API_KEYS": APIFY_API_KEYS_STR_1,
    "FIRST_WORKSPACE_SLUG": OTHER_WORKSPACE_SLUG,
}


@pytest.mark.patch_settings(SETTINGS_WORKSPACE_MAIN)
def test_get_apify_keys_main(patch_settings):
    """Test get apify keys."""
    assert utils.get_apify_api_key() == MAIN_APIFY_API_KEY


@pytest.mark.patch_settings(SETTINGS_WORKSPACE_MAIN)
def test_get_apify_keys_other(patch_settings):
    """Test get apify keys for other workspace."""
    assert utils.get_apify_api_key(OTHER_WORKSPACE_SLUG) == OTHER_APIFY_API_KEY


@pytest.mark.patch_settings(SETTINGS_WORKSPACE_OTHER)
def test_get_apify_keys_other_workspace(patch_settings):
    """Test get apify keys."""
    assert utils.get_apify_api_key() == OTHER_APIFY_API_KEY


@pytest.mark.patch_settings(SETTINGS_WORKSPACE_MAIN)
def test_get_apify_keys_not_found(patch_settings):
    """Test get apify keys."""
    with pytest.raises(ValueError):
        utils.get_apify_api_key("not_found")


@pytest.mark.patch_settings(
    {"APIFY_API_KEYS": APIFY_API_KEYS_STR_1, "FIRST_WORKSPACE_SLUG": "not_found"}
)
def test_get_apify_keys_not_found_workspace(patch_settings):
    """Test get apify keys."""
    with pytest.raises(ValueError):
        utils.get_apify_api_key()


def test_get_project_namespace():
    """Test get project namespace."""
    assert utils.get_project_namespace(1) == "project_id1"


def test_get_project_namespace_prefix():
    """Test get project namespace."""
    assert utils.get_project_namespace(1, "test_") == "test_project_id1"


@pytest.mark.parametrize(
    "project_id, namespace_prefix",
    [
        (-1, ""),
        (1, "test-"),
    ],
)
def test_get_project_namespace_invalid(project_id, namespace_prefix):
    """Test get project namespace."""
    with pytest.raises(ValueError):
        utils.get_project_namespace(project_id, namespace_prefix)
