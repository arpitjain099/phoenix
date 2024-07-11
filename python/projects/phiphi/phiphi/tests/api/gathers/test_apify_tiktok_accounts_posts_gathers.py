"""Tes Apify TikTok Accounts Posts Gathers."""
import datetime

from phiphi.api.projects.gathers import constants
from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.api.projects.gathers.apify_tiktok_accounts_posts import schemas


def test_serialize_tiktok_accounts_posts_gather_response_with_all_fields():
    """Test that ApifyTikTokAccountsPostsGatherResponse serializes correctly."""
    instance = schemas.ApifyTikTokAccountsPostsGatherResponse(
        name="Example",
        limit_posts_per_account=10,
        account_username_list=["example", "test"],
        posts_created_after="2024-04-04",
        posts_created_since_no_days=7,
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
