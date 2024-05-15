"""Test Apify Facebook Posts Gathers."""
import pytest
from fastapi.testclient import TestClient

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_facebook_comment_gather(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook comment gather."""
    data = {
        "description": "First apify gather",
        "limit_comments_per_post": 1000,
        "sort_comments_by": "facebook_default",
        "post_url_list": ["https://buildup.org"],
        "include_comment_replies": True,
        "source": "apify",
        "platform": "facebook",
        "data_type": "comments",
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_comments", json=data)
    assert response.status_code == 200
    gather = response.json()
    assert gather["description"] == data["description"]
    assert gather["project_id"] == project_id
    assert gather["sort_comments_by"] == data["sort_comments_by"]
    assert gather["limit_comments_per_post"] == data["limit_comments_per_post"]
    assert gather["include_comment_replies"] == data["include_comment_replies"]
    assert gather["post_url_list"] == data["post_url_list"]
    assert gather["platform"] == "facebook"
    assert gather["data_type"] == "comments"
    assert gather["created_at"] == CREATED_TIME


@pytest.mark.freeze_time(CREATED_TIME)
def test_data_type_apify_facebook_comment(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook comment gather.

    This test checks that if the source, platform and data type of the child gather are taken from
    the route and not the payload.
    """
    data = {
        "description": "First apify gather",
        "limit_comments_per_post": 1000,
        "sort_comments_by": "facebook_default",
        "post_url_list": ["https://buildup.org"],
        "include_comment_replies": True,
        "source": "apify",
        "platform": "facebook",
        "data_type": "posts",
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_comments", json=data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["data_type"] == "comments"
