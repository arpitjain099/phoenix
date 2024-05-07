"""Test Apify Facebook Posts Gathers."""
import pytest
from fastapi.testclient import TestClient

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_facebook_post_gather(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook gather."""
    data = {
        "description": "First apify gather",
        "limit_posts_per_account": 1000,
        "only_posts_older_than": "2022-3-5",
        "only_posts_newer_than": "2021-4-8",
        "author_url_list": ["https://buildup.org"],
        "source": "apify",
        "platform": "facebook",
        "data_type": "posts",
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_post", json=data)
    assert response.status_code == 200
    gather = response.json()
    assert gather["description"] == data["description"]
    assert gather["project_id"] == project_id
    assert gather["author_url_list"] == data["author_url_list"]
    assert gather["limit_posts_per_account"] == data["limit_posts_per_account"]
    assert gather["only_posts_older_than"] == data["only_posts_older_than"]
    assert gather["only_posts_newer_than"] == data["only_posts_newer_than"]
    assert gather["platform"] == "facebook"
    assert gather["data_type"] == "posts"
    assert gather["created_at"] == CREATED_TIME
