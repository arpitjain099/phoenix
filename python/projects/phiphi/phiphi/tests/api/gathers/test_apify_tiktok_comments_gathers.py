"""Test Apify TikTok Comments Gathers."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects import gathers
from phiphi.seed import apify_tiktok_comments_gather

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_tiktok_comments_gather(reseed_tables, client: TestClient) -> None:
    """Test create apify tiktok comment gather."""
    post_data = {
        "name": "First apify gather",
        "limit_comments_per_post": 1000,
        "post_url_list": ["https://buildup.org/"],
        "include_comment_replies": True,
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_tiktok_comments", json=post_data)
    assert response.status_code == 200
    gather = response.json()

    for key, value in post_data.items():
        assert gather[key] == value

    # These are automatically set

    assert gather["created_at"] == CREATED_TIME


def test_patch_apify_tiktok_comments(reseed_tables, client: TestClient) -> None:
    """Test patch apify tiktok comment gather."""
    data = {
        "name": "Updated apify gather",
        "limit_comments_per_post": 1,
        "post_url_list": ["https://buildup.org/2/"],
        "include_comment_replies": True,
    }
    # Check that it is not the same as the seed values
    # just in case there are changes in the seed
    test_gather = apify_tiktok_comments_gather.TEST_APIFY_TIKTOK_COMMENTS_GATHERS[0]
    project_id = test_gather.project_id
    gather_id = test_gather.id
    dict_test_gather = test_gather.dict()
    for key, value in data.items():
        assert dict_test_gather[key] != value
    response = client.patch(
        f"/projects/{project_id}/gathers/apify_tiktok_comments/{gather_id}", json=data
    )
    json_response = response.json()
    assert response.status_code == 200
    for key, value in data.items():
        assert json_response[key] == value

    assert json_response["child_type"] == "apify_tiktok_comments"


def test_serialize_tiktok_comments_gather_response_with_all_fields():
    """Test that ApifyTikTokCommentsGatherResponse serializes correctly."""
    instance = gathers.apify_tiktok_comments.schemas.ApifyTikTokCommentsGatherResponse(
        name="Example",
        post_url_list=["https://example.com", "https://test.com/"],
        limit_comments_per_post=10,
        include_comment_replies=True,
        id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_comments,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_output_dict = {
        # Be aware that Pydantic will normalise the URL to have a trailing slash
        "startUrls": ["https://example.com/", "https://test.com/"],
        "maxItems": 10,
        "includeReplies": True,
    }

    assert expected_output_dict == output_dict


def test_serialize_tiktok_comments_gather_response_with_required_fields_only():
    """Test that serialize to Apify correctly omits fields when they are not provided."""
    instance = gathers.apify_tiktok_comments.schemas.ApifyTikTokCommentsGatherResponse(
        name="Example",
        post_url_list=["https://example.com/", "https://test.com"],
        limit_comments_per_post=10,
        id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_comments,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_keys = ["startUrls"]
    assert all(key in output_dict for key in expected_keys)
    assert "limit_comments_per_post" not in output_dict

    expected_output_dict = {
        # Be aware that pydantic will normalise the URL to have a trailing slash
        "startUrls": ["https://example.com/", "https://test.com/"],
        "maxItems": 10,
    }

    assert expected_output_dict == output_dict
