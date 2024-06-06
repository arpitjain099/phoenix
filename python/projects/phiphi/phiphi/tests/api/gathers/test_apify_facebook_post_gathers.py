"""Test Apify Facebook Posts Gathers."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects import gathers
from phiphi.api.projects.gathers import child_crud

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


def test_get_gather_crud(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    gather = child_crud.get_child_gather(reseed_tables, 1, 1)
    assert gather
    assert gather.id == 1
    assert gather.project_id == 1
    assert gather.source == "apify"
    assert gather.platform == "facebook"
    assert gather.data_type == "posts"
    assert gather.limit_posts_per_account == 1000


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_facebook_post_gather(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook gather."""
    data = {
        "description": "First apify gather",
        "limit_posts_per_account": 1000,
        "only_posts_older_than": "2022-3-5",
        "only_posts_newer_than": "2021-4-8",
        "account_url_list": ["https://buildup.org/"],
        "source": "apify",
        "platform": "facebook",
        "data_type": "posts",
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_posts", json=data)
    assert response.status_code == 200
    gather = response.json()

    assert gather["description"] == data["description"]
    assert gather["project_id"] == project_id
    assert gather["account_url_list"] == data["account_url_list"]
    assert gather["limit_posts_per_account"] == data["limit_posts_per_account"]
    assert gather["only_posts_older_than"] == data["only_posts_older_than"]
    assert gather["only_posts_newer_than"] == data["only_posts_newer_than"]
    assert gather["platform"] == "facebook"
    assert gather["data_type"] == "posts"
    assert gather["created_at"] == CREATED_TIME


@pytest.mark.freeze_time(CREATED_TIME)
def test_data_type_apify_facebook_post(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook gather."""
    data = {
        "description": "First apify gather",
        "limit_posts_per_account": 1000,
        "only_posts_older_than": "2022-3-5",
        "only_posts_newer_than": "2021-4-8",
        "account_url_list": ["https://buildup.org/"],
        "source": "apify",
        "platform": "facebook",
        "data_type": "comments",
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_posts", json=data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["data_type"] == "posts"


def test_serialize_facebook_post_gather_response_with_all_fields():
    """Test that ApifyFacebookPostGatherResponse serializes correctly."""
    instance = gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse(
        description="Example",
        limit_posts_per_account=10,
        account_url_list=[
            "https://www.facebook.com/humansofnewyork/",
            "https://www.facebook.com/example_account/",
        ],
        only_posts_older_than="2024-04-04",
        only_posts_newer_than="2024-04-03",
        id=1,
        platform=gathers.schemas.Platform.facebook,
        data_type=gathers.schemas.DataType.posts,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        deleted_at=None,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_posts,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_output_dict = {
        "resultsLimit": 10,
        "startUrls": [
            {"url": "https://www.facebook.com/humansofnewyork/"},
            {"url": "https://www.facebook.com/example_account/"},
        ],
        "onlyPostsOlderThan": "2024-04-04",
        "onlyPostsNewerThan": "2024-04-03",
    }

    assert expected_output_dict == output_dict


def test_serialize_facebook_post_gather_response_with_required_fields_only():
    """Test that serialize to Apify correctly omits fields when they are not provided."""
    instance = gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse(
        description="Example",
        limit_posts_per_account=10,
        account_url_list=[
            "https://www.facebook.com/humansofnewyork/",
            "https://www.facebook.com/example_account/",
        ],
        id=1,
        platform=gathers.schemas.Platform.facebook,
        data_type=gathers.schemas.DataType.posts,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        deleted_at=None,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_posts,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_keys = ["resultsLimit", "startUrls"]
    assert all(key in output_dict for key in expected_keys)
    assert "onlyPostsOlderThan" not in output_dict
    assert "onlyPostsNewerThan" not in output_dict

    expected_output_dict = {
        "resultsLimit": 10,
        "startUrls": [
            {"url": "https://www.facebook.com/humansofnewyork/"},
            {"url": "https://www.facebook.com/example_account/"},
        ],
    }

    assert expected_output_dict == output_dict
