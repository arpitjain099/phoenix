"""Test Apify Facebook Posts Gathers."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects import gathers
from phiphi.api.projects.gathers import child_crud
from phiphi.seed import apify_facebook_posts_gather

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


def test_get_gather_crud(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    gather = child_crud.get_child_gather(reseed_tables, 1, 1)
    assert gather
    # Needed for mypy to pass
    assert isinstance(
        gather, gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse
    )
    assert gather.id == 1
    assert gather.project_id == 1
    assert gather.child_type == "apify_facebook_posts"
    assert gather.limit_posts_per_account == 1000


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_facebook_posts_gather(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook gather."""
    data = {
        "name": "First apify gather",
        "limit_posts_per_account": 1000,
        "posts_created_after": "2021-4-8",
        "posts_created_before": "2022-3-5",
        "account_url_list": ["https://buildup.org/"],
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_posts", json=data)
    assert response.status_code == 200
    gather = response.json()

    assert gather["name"] == data["name"]
    assert gather["project_id"] == project_id
    assert gather["account_url_list"] == data["account_url_list"]
    assert gather["limit_posts_per_account"] == data["limit_posts_per_account"]
    assert gather["posts_created_after"] == data["posts_created_after"]
    assert gather["posts_created_before"] == data["posts_created_before"]
    assert gather["created_at"] == CREATED_TIME


def test_patch_apify_facebook_posts(reseed_tables, client: TestClient) -> None:
    """Test patch apify facebook comment gather."""
    data = {
        "name": "Updated apify gather",
        "limit_posts_per_account": 1,
        "account_url_list": ["https://buildup.org/2/"],
        "posts_created_after": "2021-4-8",
        "posts_created_before": "2022-3-5",
    }
    # Check that it is not the same as the seed values
    # just in case there are changes in the seed
    expected_gather = apify_facebook_posts_gather.TEST_APIFY_FACEBOOK_POSTS_GATHER_CREATE.dict()
    for key, value in data.items():
        assert expected_gather[key] != value
    project_id = 1
    response = client.patch(f"/projects/{project_id}/gathers/apify_facebook_posts/1/", json=data)
    json_response = response.json()
    assert response.status_code == 200
    for key, value in data.items():
        assert json_response[key] == value


def test_patch_apify_facebook_posts_optional(reseed_tables, client: TestClient) -> None:
    """Test patch apify facebook comment gather check optional."""
    data = {
        "limit_posts_per_account": 2,
    }
    project_id = 1
    response = client.patch(f"/projects/{project_id}/gathers/apify_facebook_posts/1/", json=data)
    json_response = response.json()
    assert response.status_code == 200
    expected_gather = apify_facebook_posts_gather.TEST_APIFY_FACEBOOK_POSTS_GATHER_CREATE.dict()
    expected_gather["limit_posts_per_account"] = 2
    for key, value in expected_gather.items():
        assert json_response[key] == value


def test_patch_apify_facebook_posts_invalid(reseed_tables, client: TestClient) -> None:
    """Test patch apify facebook comment gather posts invalid."""
    data = {
        # values that we shouldn't be able to set in the model
        "child_type": "apify",
        "created_at": "2024-01-01",
        # Not in any schema
        "not_included_allowed": 2,
    }
    project_id = 1
    for key, value in data.items():
        response = client.patch(
            f"/projects/{project_id}/gathers/apify_facebook_posts/1/", json={key: value}
        )
        assert response.status_code == 422


@pytest.mark.freeze_time(CREATED_TIME)
def test_data_type_apify_facebook_posts(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook gather."""
    data = {
        "name": "First apify gather",
        "limit_posts_per_account": 1000,
        "posts_created_after": "2022-3-5",
        "posts_created_before": "2021-4-8",
        "account_url_list": ["https://buildup.org/"],
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_posts", json=data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["child_type"] == "apify_facebook_posts"


def test_serialize_facebook_post_gather_response_with_all_fields():
    """Test that ApifyFacebookPostsGatherResponse serializes correctly."""
    instance = gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse(
        name="Example",
        limit_posts_per_account=10,
        account_url_list=[
            "https://www.facebook.com/humansofnewyork/",
            "https://www.facebook.com/example_account/",
        ],
        posts_created_after="2024-04-03",
        posts_created_before="2024-04-04",
        id=1,
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
        "onlyPostsNewerThan": "2024-04-03",
        "onlyPostsOlderThan": "2024-04-04",
    }

    assert expected_output_dict == output_dict


def test_serialize_facebook_post_gather_response_with_required_fields_only():
    """Test that serialize to Apify correctly omits fields when they are not provided."""
    instance = gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse(
        name="Example",
        limit_posts_per_account=10,
        account_url_list=[
            "https://www.facebook.com/humansofnewyork/",
            "https://www.facebook.com/example_account/",
        ],
        id=1,
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
