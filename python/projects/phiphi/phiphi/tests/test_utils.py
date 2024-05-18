"""Test utils."""
import pytest

from phiphi import utils

APIFY_API_KEYS_STR_1 = '{"main": "main_test", "test": "test_test"}'
SETTINGS_ENV_MAIN = {"APIFY_API_KEYS": APIFY_API_KEYS_STR_1, "FIRST_ENVIRONMENT_SLUG": "main"}
SETTINGS_ENV_TEST = {"APIFY_API_KEYS": APIFY_API_KEYS_STR_1, "FIRST_ENVIRONMENT_SLUG": "test"}


@pytest.mark.patch_settings(SETTINGS_ENV_MAIN)
def test_get_apify_keys_main(patch_settings):
    """Test get apify keys."""
    assert utils.get_apify_api_key() == "main_test"


@pytest.mark.patch_settings(SETTINGS_ENV_MAIN)
def test_get_apify_keys_test(patch_settings):
    """Test get apify keys."""
    assert utils.get_apify_api_key("test") == "test_test"


@pytest.mark.patch_settings(SETTINGS_ENV_TEST)
def test_get_apify_keys_test_env(patch_settings):
    """Test get apify keys."""
    assert utils.get_apify_api_key() == "test_test"


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
