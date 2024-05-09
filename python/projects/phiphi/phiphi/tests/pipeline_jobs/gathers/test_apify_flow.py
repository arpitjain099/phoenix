"""Tests for Apify gathers."""

from phiphi.pipeline_jobs.gathers import apify_flow, apify_input_schemas


def manual_test_trigger_apify_scrape_and_batch_download():
    """Manually test the trigger_apify_scrape_and_batch_download_results flow.

    WARNING: this will incur costs on Apify.

    To use this test, replace "MY_APIFY_TOKEN" with your own Apify API token, and then function
    manually.
    """
    run_input = apify_input_schemas.ApifyFacebookPostsInput(
        only_posts_older_than="2024-04-04",
        only_posts_newer_than="2024-01-03",
        results_per_url_limit=4,
        account_urls=[
            "https://www.facebook.com/howtobuildup/",
            "https://www.facebook.com/unitednations/",
        ],
    )

    apify_flow.trigger_apify_scrape_and_batch_download_results(
        apify_token="MY_APIFY_TOKEN",
        data_type="posts",
        run_input=run_input,
        batch_size=3,
    )
