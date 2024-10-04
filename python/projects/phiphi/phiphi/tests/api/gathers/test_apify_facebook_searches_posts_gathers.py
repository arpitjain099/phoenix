"""Test Apify Facebook Searches Posts Gathers."""
import pydantic
import pytest

from phiphi.api.projects import gathers


def test_validation_apify_proxy_config():
    """Test that ApifyProxyConfig throws an error if use_apify_proxy is False."""
    with pytest.raises(pydantic.ValidationError):
        gathers.apify_facebook_searches_posts.schemas.ApifyProxyConfig(
            use_apify_proxy=False, apify_proxy_groups=["GROUP1", "GROUP2"]
        )
