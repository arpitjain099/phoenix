"""Test Apify Facebook Posts Gathers."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects import gathers
from phiphi.api.projects.gathers import child_crud
from phiphi.seed import apify_facebook_comments

CREATED_TIME = "2024-04-01T12:00:01"
UPDATE_TIME = "2024-04-01T12:00:02"


def test_get_gather_crud(client: TestClient, reseed_tables) -> None:
    """Test getting gathers."""
    gather = child_crud.get_child_gather(reseed_tables, 2, 4)
    assert gather
    assert gather.id == 4
    assert gather.project_id == 2
    assert gather.source == "apify"
    assert gather.platform == "facebook"
    assert gather.data_type == "comments"
    assert gather.limit_comments_per_post == 1000


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_facebook_comment_gather(reseed_tables, client: TestClient) -> None:
    """Test create apify facebook comment gather."""
    data = {
        "name": "First apify gather",
        "limit_comments_per_post": 1000,
        "sort_comments_by": "facebook_default",
        "post_url_list": ["https://buildup.org/"],
        "include_comment_replies": True,
        "source": "apify",
        "platform": "facebook",
        "data_type": "comments",
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/gathers/apify_facebook_comments", json=data)
    assert response.status_code == 200
    gather = response.json()

    assert gather["name"] == data["name"]
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
        "name": "First apify gather",
        "limit_comments_per_post": 1000,
        "sort_comments_by": "facebook_default",
        "post_url_list": ["https://buildup.org/"],
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


def test_patch_apify_facebook_comment(reseed_tables, client: TestClient) -> None:
    """Test patch apify facebook comment gather."""
    data = {
        "name": "Updated apify gather",
        "limit_comments_per_post": 1,
        "sort_comments_by": "most_relevant",
        "post_url_list": ["https://buildup.org/2/"],
        "include_comment_replies": True,
    }
    # Check that it is not the same as the seed values
    # just in case there are changes in the seed
    expected_gather = apify_facebook_comments.TEST_APIFY_FACEBOOK_COMMENT_GATHER_CREATE.dict()
    for key, value in data.items():
        assert expected_gather[key] != value
    project_id = 2
    response = client.patch(
        f"/projects/{project_id}/gathers/apify_facebook_comments/4/", json=data
    )
    json_response = response.json()
    assert response.status_code == 200
    for key, value in data.items():
        assert json_response[key] == value


def test_patch_apify_facebook_comment_invalid(reseed_tables, client: TestClient) -> None:
    """Test patch apify facebook comment gather invalid."""
    data = {
        "source": "apify",
        "platform": "facebook",
        "data_type": "comments",
        "not_included_allowed": "not_allowed",
    }
    project_id = 2
    for key, value in data.items():
        response = client.patch(
            f"/projects/{project_id}/gathers/apify_facebook_comments/4/", json={key: value}
        )
        assert response.status_code == 422


def test_serialize_facebook_comment_gather_response_with_all_fields():
    """Test that ApifyFacebookCommentsGatherResponse serializes correctly."""
    instance = gathers.apify_facebook_comments.schemas.ApifyFacebookCommentsGatherResponse(
        name="Example",
        limit_comments_per_post=25,
        post_url_list=[
            "https://www.facebook.com/post1",
            "https://www.facebook.com/post2",
        ],
        sort_comments_by=gathers.apify_facebook_comments.schemas.FacebookCommentSortOption.most_relevant,
        include_comment_replies=True,
        id=1,
        platform=gathers.schemas.Platform.facebook,
        data_type=gathers.schemas.DataType.comments,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        deleted_at=None,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_comments,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_output_dict = {
        "resultsLimit": 25,
        "startUrls": [
            {"url": "https://www.facebook.com/post1"},
            {"url": "https://www.facebook.com/post2"},
        ],
        "viewOption": "RANKED_THREADED",
        "includeNestedComments": True,
    }

    assert expected_output_dict == output_dict


def test_serialize_facebook_comment_gather_response_with_required_fields_only():
    """Test that serialize to Apify correctly omits fields when they are not provided."""
    instance = gathers.apify_facebook_comments.schemas.ApifyFacebookCommentsGatherResponse(
        name="Example",
        limit_comments_per_post=25,
        post_url_list=[
            "https://www.facebook.com/post1",
            "https://www.facebook.com/post2",
        ],
        id=1,
        platform=gathers.schemas.Platform.facebook,
        data_type=gathers.schemas.DataType.comments,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        deleted_at=None,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_comments,
    )

    output_dict = instance.serialize_to_apify_input()

    # Checking if the keys related to the sort option and nested comments are not present
    # since they weren't initialized.
    expected_keys = ["resultsLimit", "startUrls"]
    assert all(key in output_dict for key in expected_keys)
    assert "viewOption" not in output_dict
    assert "includeNestedComments" not in output_dict

    expected_output_dict = {
        "resultsLimit": 25,
        "startUrls": [
            {"url": "https://www.facebook.com/post1"},
            {"url": "https://www.facebook.com/post2"},
        ],
    }

    assert expected_output_dict == output_dict
