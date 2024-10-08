"""Test Apify Facebook Search Posts Gathers."""
import datetime

import pydantic
import pytest
from pydantic_extra_types.country import CountryAlpha2

from phiphi.api.projects import gathers


def test_validation_apify_proxy_config():
    """Test that ApifyProxyConfig throws an error if use_apify_proxy is False."""
    with pytest.raises(pydantic.ValidationError):
        gathers.apify_facebook_search_posts.schemas.ApifyProxyConfig(
            use_apify_proxy=False, apify_proxy_groups=["GROUP1", "GROUP2"]
        )


def test_validation_apify_proxy_config_country():
    """Test that ApifyProxyConfig throws validation error with in correct country code."""
    with pytest.raises(pydantic.ValidationError):
        gathers.apify_facebook_search_posts.schemas.ApifyProxyConfig(
            use_apify_proxy=True,
            apify_proxy_groups=["GROUP1", "GROUP2"],
            apify_proxy_country="NOT_A_COUNTRY",  # type: ignore[arg-type]
        )


def test_serialize_facebook_search_post_gather_response_with_all_fields():
    """Test that ApifyFacebookSearchPostsGatherResponse serializes correctly."""
    instance = gathers.apify_facebook_search_posts.schemas.ApifyFacebookSearchPostsGatherResponse(
        name="Example",
        id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_search_posts,
        search_query="hello",
        limit_posts=10,
        limit_retries=5,
        recent_posts=False,
        proxy=gathers.apify_facebook_search_posts.schemas.ApifyProxyConfig(
            use_apify_proxy=True,
            apify_proxy_groups=["GROUP1", "GROUP2"],
            apify_proxy_country=CountryAlpha2("US"),
        ),
    )

    output_dict = instance.serialize_to_apify_input()

    expected_output_dict = {
        "query": "hello",
        "max_posts": 10,
        "max_retries": 5,
        "recent_posts": False,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["GROUP1", "GROUP2"],
            "apifyProxyCountry": "US",
        },
        # This attribute is added with the serialisation
        "search_type": gathers.constants.FACEBOOK_POST_SEARCH_TYPE,
    }

    assert expected_output_dict == output_dict


def test_serialize_facebook_search_post_gather_response_with_required_fields_only():
    """Test that serialize to Apify correctly omits fields when they are not provided."""
    instance = gathers.apify_facebook_search_posts.schemas.ApifyFacebookSearchPostsGatherResponse(
        name="Example",
        id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_search_posts,
        search_query="hello",
        limit_posts=10,
        limit_retries=5,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_output_dict = {
        "query": "hello",
        "max_posts": 10,
        "max_retries": 5,
        "search_type": gathers.constants.FACEBOOK_POST_SEARCH_TYPE,
    }

    assert expected_output_dict == output_dict
