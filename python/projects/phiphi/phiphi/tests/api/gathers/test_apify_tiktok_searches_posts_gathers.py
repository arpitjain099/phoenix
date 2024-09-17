"""Test Apify TikTok Searches Posts Gathers."""
import datetime

from phiphi.api.projects import gathers


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
