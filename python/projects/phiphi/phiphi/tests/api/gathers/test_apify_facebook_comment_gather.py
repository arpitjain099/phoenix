"""Test Apify Facebook Posts Gathers."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects import gathers

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


def test_serialize_facebook_comment_gather_response_with_all_fields():
    """Test that ApifyFacebookCommentGatherResponse serializes correctly."""
    instance = gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse(
        description="Example",
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
    instance = gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse(
        description="Example",
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
