"""Tests for Apify gathers."""
import datetime
import json

import pandas as pd
import pytest
from prefect.logging import disable_run_logger as disable_prefect_run_logger

from phiphi import config
from phiphi.api.projects import gathers
from phiphi.pipeline_jobs.gathers import apify_input_schemas, apify_scrape


def facebook_posts_gather_example() -> (
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse
):
    """Example for ApifyFacebookPostGatherResponse schema."""
    return gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse(
        description="Example",
        limit_posts_per_account=4,
        account_url_list=[
            "https://www.facebook.com/howtobuildup/",
            "https://www.facebook.com/unitednations/",
        ],
        only_posts_older_than="2024-04-04",
        only_posts_newer_than="2024-01-03",
        id=1,
        platform=gathers.schemas.Platform.facebook,
        data_type=gathers.schemas.DataType.posts,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        deleted_at=None,
        latest_job_run=None,
    )


def facebook_comments_gather_example() -> (
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse
):
    """Example for ApifyFacebookCommentGatherResponse schema."""
    return gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse(
        description="Example",
        limit_comments_per_post=4,
        post_url_list=[
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml",
        ],
        sort_comments_by=gathers.apify_facebook_comments.schemas.FacebookCommentSortOption.facebook_default,
        include_comment_replies=False,
        id=1,
        platform=gathers.schemas.Platform.facebook,
        data_type=gathers.schemas.DataType.comments,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        deleted_at=None,
        latest_job_run=None,
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

    WARNING: this will incur costs on Apify (unless use have configured the mock settings).
    WARNING: this will write to BigQuery (unless you have configured the mock settings).

    To use this test:
    - ensure that a valid Apify token is set in the config - you should use your personal token not
      the org token ideally
    - change `gather` to the corresponding desired Apify actor to test
    - run the function manually
    """
    gather = facebook_comments_gather_example()
    apify_scrape.apify_scrape_and_batch_download_results(
        gather=gather,
        job_run_id=1,
        bigquery_dataset="test_dataset",
        bigquery_table="test_table",
        batch_size=3,
    )


@pytest.mark.patch_settings(
    {
        "USE_MOCK_APIFY": True,
        "USE_MOCK_BQ": True,
        "APIFY_API_KEYS": {"main": "dummy_key"},
    }
)
def test_mock_apify_scrape_and_batch_download_results(tmpdir, patch_settings, mocker):
    """Test apify_scrape_and_batch_download_results with mocked out Apify function."""
    mocker.patch.object(config.settings, "MOCK_BQ_ROOT_DIR", str(tmpdir))

    with disable_prefect_run_logger():
        apify_scrape.apify_scrape_and_batch_download_results.fn(
            gather=facebook_posts_gather_example(),
            job_run_id=1,
            batch_size=3,
            bigquery_dataset="test_dataset",
            bigquery_table="test_table",
        )

    # Check that the parquet file was written
    parquet_file_path = tmpdir.join("test_dataset", "test_table.parquet")
    assert parquet_file_path.check()

    # Load the parquet file and verify its contents
    read_df = pd.read_parquet(parquet_file_path)
    assert not read_df.empty
    assert "project_id" in read_df.columns
    assert read_df["project_id"].iloc[0] == 1
    assert "json_data" in read_df.columns
    assert json.loads(read_df["json_data"].iloc[0])  # Ensure JSON data is valid
    assert read_df["batch_id"].iloc[0] == 0
    assert read_df["batch_id"].iloc[2] == 2
    assert len(read_df) == 3  # Note this depends on the sample data
