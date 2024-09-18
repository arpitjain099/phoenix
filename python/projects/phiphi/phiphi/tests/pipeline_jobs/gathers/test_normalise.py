"""Tests for the normalise module."""
from datetime import datetime
from unittest import mock

import pandas as pd
import pytest
from prefect.logging import disable_run_logger as disable_prefect_run_logger

from phiphi import config
from phiphi.api.projects.gathers import schemas
from phiphi.pipeline_jobs.gathers import apify_scrape, normalise, normalisers, utils


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normalise_batch(normalised_facebook_posts_df, facebook_posts_gather_fixture):
    """Test normalise_batch function."""
    batch_json = utils.load_sample_raw_data(
        child_type_name=schemas.ChildTypeName.apify_facebook_posts
    )

    processed_df = normalise.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_posts_json,
        batch_json=batch_json,
        gather_id=facebook_posts_gather_fixture.id,
        gather_child_type=facebook_posts_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_facebook_posts_df)


@pytest.mark.patch_settings(
    {
        "USE_MOCK_APIFY": True,
        "USE_MOCK_BQ": True,
        "APIFY_API_KEYS": {"main": "dummy_key"},
    }
)
def test_normalise_batches(
    tmpdir,
    patch_settings,
    mocker,
    facebook_posts_gather_fixture,
    normalised_facebook_posts_df,
    freezer,
):
    """Test normalise_batches function."""
    # Set up mock BigQuery root directory
    mocker.patch.object(config.settings, "MOCK_BQ_ROOT_DIR", str(tmpdir))

    freezer.move_to("2024-04-01T12:00:00.000Z")
    # First, run the scrape and batch download results function
    with disable_prefect_run_logger():
        apify_scrape.apify_scrape_and_batch_download_results.fn(
            gather=facebook_posts_gather_fixture,
            job_run_id=1,
            batch_size=3,
            bigquery_dataset="test_dataset",
            bigquery_table="gather_batches",
        )

    # Check that the parquet file was written
    parquet_file_path = tmpdir.join("test_dataset", "gather_batches.parquet")
    assert parquet_file_path.check()

    freezer.move_to("2024-04-02T12:10:59.000Z")
    # Now, run the normalise_batches function
    with disable_prefect_run_logger():
        normalise.normalise_batches.fn(
            gather_id=facebook_posts_gather_fixture.id,
            job_run_id=1,
            bigquery_dataset="test_dataset",
        )

    # Check that the normalized data was written to the correct Parquet file
    parquet_file_path = tmpdir.join("test_dataset", "generalised_messages.parquet")
    assert parquet_file_path.check()

    # Alter expected DataFrame to match that now using multiple batches
    normalised_facebook_posts_df["gather_batch_id"] = [0, 0, 0, 1, 1, 1, 2, 2]

    # Load the parquet file and verify its contents
    processed_df = pd.read_parquet(parquet_file_path)
    pd.testing.assert_frame_equal(processed_df, normalised_facebook_posts_df)


@mock.patch("phiphi.pipeline_jobs.gathers.utils.load_sample_raw_data")
@pytest.mark.patch_settings(
    {
        "USE_MOCK_APIFY": True,
        "USE_MOCK_BQ": True,
        "APIFY_API_KEYS": {"main": "dummy_key"},
    }
)
def test_normalise_error_batch(
    mock_load_sample_raw_data,
    tmpdir,
    patch_settings,
    mocker,
    tiktok_accounts_posts_gather_fixture,
    normalised_facebook_posts_df,
    freezer,
):
    """Test normalise_batches does not crash when a batch only has error data in it."""
    # Set up mock BigQuery root directory
    mocker.patch.object(config.settings, "MOCK_BQ_ROOT_DIR", str(tmpdir))
    mock_load_sample_raw_data.return_value = [
        {
            "url": "https://www.tiktok.com/channel/@username",
            "input": "https://www.tiktok.com/channel/@username",
            "error": "The provided profile URL is not a valid TikTok profile URL: }",
        },
    ]
    freezer.move_to("2024-04-01T12:00:00.000Z")
    # First, run the scrape and batch download results function
    with disable_prefect_run_logger():
        apify_scrape.apify_scrape_and_batch_download_results.fn(
            gather=tiktok_accounts_posts_gather_fixture,
            job_run_id=1,
            batch_size=3,
            bigquery_dataset="test_dataset",
            bigquery_table="gather_batches",
        )

    # Check that the parquet file was written
    parquet_file_path = tmpdir.join("test_dataset", "gather_batches.parquet")
    assert parquet_file_path.check()

    freezer.move_to("2024-04-02T12:10:59.000Z")
    # Now, run the normalise_batches function
    with disable_prefect_run_logger():
        normalise.normalise_batches.fn(
            gather_id=tiktok_accounts_posts_gather_fixture.id,
            job_run_id=1,
            bigquery_dataset="test_dataset",
        )

    # Check that no error was thrown, and no normalized data was written as the raw data was not
    # valid
    parquet_file_path = tmpdir.join("test_dataset", "generalised_messages.parquet")
    assert not parquet_file_path.check()
