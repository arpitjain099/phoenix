"""Tes Apify TikTok Accounts Posts Gathers."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects.gathers import constants
from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.api.projects.gathers.apify_tiktok_accounts_posts import schemas

CREATED_TIME = "2024-04-01T12:00:01"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_apify_tiktok_accounts_posts_gather(reseed_tables, client: TestClient) -> None:
    """Test create apify TikTok accounts posts gather."""
    data = {
        "name": "First apify gather",
        "limit_posts_per_account": 1000,
        "account_username_list": ["example"],
    }
    project_id = 1
    response = client.post(
        f"/projects/{project_id}/gathers/apify_tiktok_accounts_posts", json=data
    )
    assert response.status_code == 200
    gather = response.json()

    assert gather["name"] == data["name"]
    assert gather["project_id"] == project_id
    assert gather["account_username_list"] == data["account_username_list"]
    assert gather["limit_posts_per_account"] == data["limit_posts_per_account"]
    # These are automatically set
    assert gather["source"] == "apify"
    assert gather["platform"] == "tiktok"
    assert gather["data_type"] == "posts"
    assert gather["created_at"] == CREATED_TIME


def test_serialize_tiktok_accounts_posts_gather_response_with_all_fields():
    """Test that ApifyTikTokAccountsPostsGatherResponse serializes correctly."""
    instance = schemas.ApifyTikTokAccountsPostsGatherResponse(
        name="Example",
        limit_posts_per_account=10,
        account_username_list=["example", "test"],
        posts_created_after="2024-04-04",
        posts_created_since_num_days=7,
        proxy_country_to_gather_from="US",
        id=1,
        platform=gather_schemas.Platform.tiktok,
        data_type=gather_schemas.DataType.posts,
        source=gather_schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        deleted_at=None,
        latest_job_run=None,
        child_type=gather_schemas.ChildTypeName.apify_tiktok_hashtags_posts,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_output_dict = {
        "resultsPerPage": 10,
        "profiles": ["example", "test"],
        "oldestPostDate": "2024-04-04",
        "scrapeLastNDays": 7,
        "proxyCountryCode": "US",
        "searchSection": constants.TIKTOK_POST_SEARCH_SECTION,
    }

    assert expected_output_dict == output_dict


def test_serialize_tiktok_accounts_posts_gather_response_with_required_fields_only():
    """Test that serialize to Apify correctly omits fields when they are not provided."""
    instance = schemas.ApifyTikTokAccountsPostsGatherResponse(
        name="Example",
        limit_posts_per_account=10,
        account_username_list=["example", "test"],
        id=1,
        platform=gather_schemas.Platform.tiktok,
        data_type=gather_schemas.DataType.posts,
        source=gather_schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=123,
        deleted_at=None,
        latest_job_run=None,
        child_type=gather_schemas.ChildTypeName.apify_tiktok_hashtags_posts,
    )

    output_dict = instance.serialize_to_apify_input()

    expected_keys = ["resultsPerPage", "profiles", "searchSection"]
    assert all(key in output_dict for key in expected_keys)
    assert "oldestPostDate" not in output_dict
    assert "scrapeLastNDays" not in output_dict
    assert "proxyCountryCode" not in output_dict

    expected_output_dict = {
        "resultsPerPage": 10,
        "profiles": ["example", "test"],
        "searchSection": constants.TIKTOK_POST_SEARCH_SECTION,
    }

    assert expected_output_dict == output_dict
