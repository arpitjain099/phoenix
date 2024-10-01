"""Test Apify TikTok Searches Posts Gathers."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects import gathers
from phiphi.seed import apify_tiktok_searches_posts_gather

CREATED_TIME = "2024-06-01T12:00:01"


@pytest.mark.parametrize(
    "post_data",
    [
        {
            "name": "First apify gather",
            "limit_posts_per_search": 1000,
            "search_list": ["example"],
        },
    ],
)
@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_tiktok_searches_posts_gather(
    reseed_tables, client: TestClient, post_data
) -> None:
    """Test create apify TikTok searches posts gather."""
    project_id = 1
    response = client.post(
        f"/projects/{project_id}/gathers/apify_tiktok_searches_posts", json=post_data
    )
    assert response.status_code == 200
    gather = response.json()

    for key, value in post_data.items():
        assert gather[key] == value

    # These are automatically set
    assert gather["created_at"] == CREATED_TIME


def test_patch_apify_tiktok_searches_posts(reseed_tables, client: TestClient) -> None:
    """Test patch apify TikTok searches posts gather."""
    data = {
        "name": "Updated apify gather",
        "search_list": ["example"],
        "limit_posts_per_search": 1,
    }
    test_gather = apify_tiktok_searches_posts_gather.TEST_APIFY_TIKTOK_SEARCHES_POSTS_GATHERS[0]
    project_id = test_gather.project_id
    gather_id = test_gather.id
    dict_test_gather = test_gather.dict()
    for key, value in data.items():
        assert dict_test_gather[key] != value
    response = client.patch(
        f"/projects/{project_id}/gathers/apify_tiktok_searches_posts/{gather_id}", json=data
    )
    assert response.status_code == 200
    gather = response.json()

    assert gather["name"] == data["name"]
    assert gather["search_list"] == data["search_list"]
    assert gather["limit_posts_per_search"] == data["limit_posts_per_search"]


def test_serialize_tiktok_searches_posts_gather_response_with_all_fields():
    """Test that ApifyTikTokSearchesPostsGatherResponse serializes correctly."""
    instance = gathers.apify_tiktok_searches_posts.schemas.ApifyTikTokSearchesPostsGatherResponse(
        name="Example",
        limit_posts_per_search=10,
        search_list=["example", "test"],
        proxy_country_to_gather_from="US",
        id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_searches_posts,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_output_dict = {
        "resultsPerPage": 10,
        "searchQueries": ["example", "test"],
        "proxyCountryCode": "US",
        "searchSection": gathers.constants.TIKTOK_POST_SEARCH_SECTION,
    }

    assert expected_output_dict == output_dict


def test_serialize_tiktok_searches_posts_gather_response_with_required_fields_only():
    """Test that serialize to Apify correctly omits fields when they are not provided."""
    instance = gathers.apify_tiktok_searches_posts.schemas.ApifyTikTokSearchesPostsGatherResponse(
        name="Example",
        limit_posts_per_search=10,
        search_list=["example", "test"],
        id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_searches_posts,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_keys = ["resultsPerPage", "searchQueries", "searchSection"]
    assert all(key in output_dict for key in expected_keys)
    assert "proxyCountryCode" not in output_dict

    expected_output_dict = {
        "resultsPerPage": 10,
        "searchQueries": ["example", "test"],
        "searchSection": gathers.constants.TIKTOK_POST_SEARCH_SECTION,
    }

    assert expected_output_dict == output_dict
