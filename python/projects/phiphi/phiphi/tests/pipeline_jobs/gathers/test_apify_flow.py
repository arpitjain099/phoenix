"""Tests for Apify gathers."""
import pytest
from prefect.logging import disable_run_logger as disable_prefect_run_logger

from phiphi.pipeline_jobs.gathers import apify_flow, apify_input_schemas


def facebook_posts_input_example() -> apify_input_schemas.ApifyFacebookPostsInput:
    """Example input for the ApifyFacebookPostsInput schema."""
    return apify_input_schemas.ApifyFacebookPostsInput(
        only_posts_older_than="2024-04-04",
        only_posts_newer_than="2024-01-03",
        results_per_url_limit=4,
        account_urls=[
            "https://www.facebook.com/howtobuildup/",
            "https://www.facebook.com/unitednations/",
        ],
    )


def facebook_comments_input_example() -> apify_input_schemas.ApifyFacebookCommentsInput:
    """Example input for the ApifyFacebookCommentsInput schema."""
    return apify_input_schemas.ApifyFacebookCommentsInput(
        post_urls=[
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml",
        ],
        results_limit=4,
    )


def tiktok_posts_input_example() -> apify_input_schemas.ApifyTiktokPostsInput:
    """Example input for the ApifyTiktokPostsInput schema."""
    return apify_input_schemas.ApifyTiktokPostsInput(
        hashtags=["#peacebuilding"],
        profiles=["@unitednations"],
        results_per_page=4,
    )


def tiktok_comments_input_example() -> apify_input_schemas.ApifyTiktokCommentsInput:
    """Example input for the ApifyTiktokCommentsInput schema."""
    return apify_input_schemas.ApifyTiktokCommentsInput(
        post_urls=[
            "https://www.tiktok.com/@unitednations/video/7369984375460498734",
            "https://www.tiktok.com/@unitednations/video/7368916231921126702",
        ],
        comments_per_post=4,
    )


def manual_test_apify_scrape_and_batch_download():
    """Manually test the apify_scrape_and_batch_download_results flow.

    WARNING: this will incur costs on Apify.

    To use this test:
    - replace "MY_APIFY_TOKEN" with your own Apify API token
    - change the input fixture to the corresponding desired Apify actor to test
    - run the function manually
    """
    run_input = facebook_comments_input_example()
    apify_flow.apify_scrape_and_batch_download_results(
        apify_token="MY_APIFY_TOKEN",
        run_input=run_input,
        batch_size=3,
    )


@pytest.mark.patch_settings({"USE_MOCK_APIFY": True})
def test_mock_apify_scrape_and_batch_download_results(tmpdir, patch_settings):
    """Test apify_scrape_and_batch_download_results with mocked out Apify function."""
    with disable_prefect_run_logger():
        apify_flow.apify_scrape_and_batch_download_results.fn(
            apify_token="NOT_A_TOKEN",
            run_input=facebook_posts_input_example(),
            batch_size=3,
            dev_batch_dir=tmpdir,
        )
