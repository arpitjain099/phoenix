"""Test Apify TikTok Comments Gathers."""
import datetime

from phiphi.api.projects import gathers


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
