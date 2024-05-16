"""Tests for the Apify gather schemas."""

from phiphi.pipeline_jobs.gathers import apify_input_schemas as schemas


def test_facebook_posts_scraper_input_to_dict():
    """Test that ApifyFacebookPostsInput converts correctly to dict for Apify call."""
    instance = schemas.ApifyFacebookPostsInput(
        only_posts_older_than="2024-04-04",
        only_posts_newer_than="2024-04-03",
        results_per_url_limit=10,
        account_urls=[
            "https://www.facebook.com/humansofnewyork/",
            "https://www.facebook.com/example_account/",
        ],
    )

    output_dict = instance.dict(by_alias=True)

    expected_output_dict = {
        "onlyPostsOlderThan": "2024-04-04",
        "onlyPostsNewerThan": "2024-04-03",
        "resultsLimit": 10,
        "startUrls": [
            {"url": "https://www.facebook.com/humansofnewyork/"},
            {"url": "https://www.facebook.com/example_account/"},
        ],
    }

    assert expected_output_dict == output_dict
