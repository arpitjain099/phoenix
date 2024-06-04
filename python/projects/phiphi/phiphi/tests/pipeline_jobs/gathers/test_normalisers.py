"""Tests for the normalisers module."""
from datetime import datetime

import pandas as pd
import pytest
from prefect.logging import disable_run_logger as disable_prefect_run_logger

from phiphi import config
from phiphi.api.projects.gathers import schemas
from phiphi.pipeline_jobs.gathers import apify_scrape, normalisers, utils


@pytest.fixture
def expected_dataframe():
    """Return the expected DataFrame based on the processed JSON data."""
    data = {
        "pi_platform_message_id": [
            "843404157832210",
            "837532328419393",
            "818337297005563",
            "824283126394381",
            "823689576453736",
            "823537799802247",
            "817481123757847",
            "823003113189049",
        ],
        "pi_platform_message_author_id": [
            "100064878993116",
            "100064878993116",
            "100064878993116",
            "100064381045972",
            "100064381045972",
            "100064381045972",
            "100064878993116",
            "100064381045972",
        ],
        "pi_platform_message_author_name": [
            "Build Up",
            "Build Up",
            "Build Up",
            "United Nations",
            "United Nations",
            "United Nations",
            "Build Up",
            "United Nations",
        ],
        "pi_platform_parent_message_id": [None, None, None, None, None, None, None, None],
        "pi_text": [
            "🗓️✒️ \nhttps://buff.ly/47Bz0N9 👀",
            "... the out! 🚀🎉 \n\n🍿 ",
            "Should digital platforms? 💥",
            "facts.\n\nDefending democracy.\n\nvia",
            "environment. https://www.un.org/en/messengers-peace/jane-goodall",
            "all times.",
            "💡Be initiatives",
            "round the world.",
        ],
        "pi_platform_message_url": [
            "https://www.facebook.com/howtobuildup/posts/pfbid0wY5Xr9MbMh6Vtfd1fjhgCBCvmtTMpYpiQBENdy3kZen1tqyHc7KRR1AXqMVbtRoXl",
            "https://www.facebook.com/howtobuildup/posts/pfbid0Pgnmi21mzGgyWgckpc6Rrz2JfzuDM8SAnyXFPzUR7bkef6fbcAfiKgzEkwftJR5Wl",
            "https://www.facebook.com/howtobuildup/posts/pfbid02ubha39CEo7VofcosVvZ1oKXnyVxNrJK9L2DtPkZkeJKS76qzmaF1etSxtVEG2fiWl",
            "https://www.facebook.com/unitednations/posts/pfbid0eCoKhMP3ssi9fxqUT22C422scmU13UfrgWcquVwN5S3g35K5NdA42cbXWEipQyjdl",
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl",
            "https://www.facebook.com/unitednations/posts/pfbid02qcW6e6RMSDQ5DT1ZB2o19N9zMBRdETnskgEyEGoLdPCMdxd7jr8ip7KK1JA8cgW5l",
            "https://www.facebook.com/howtobuildup/posts/pfbid0SJ9vqgSJsF7x1RFQjr3yp7rgYNumzJmJW7A5Xa8wEDTWuX21b2HkA4HyCH8fiaLPl",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml",
        ],
        "platform_message_last_updated_at": [
            datetime.fromisoformat("2024-04-03T06:00:25.000Z"),
            datetime.fromisoformat("2024-03-25T07:00:17.000Z"),
            datetime.fromisoformat("2024-02-22T16:00:01.000Z"),
            datetime.fromisoformat("2024-04-03T18:02:22.000Z"),
            datetime.fromisoformat("2024-04-03T08:02:00.000Z"),
            datetime.fromisoformat("2024-04-02T18:04:00.000Z"),
            datetime.fromisoformat("2024-02-21T08:00:10.000Z"),
            datetime.fromisoformat("2024-04-02T08:07:30.000Z"),
        ],
        "phoenix_platform_message_id": [
            normalisers.anonymize("843404157832210"),
            normalisers.anonymize("837532328419393"),
            normalisers.anonymize("818337297005563"),
            normalisers.anonymize("824283126394381"),
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823537799802247"),
            normalisers.anonymize("817481123757847"),
            normalisers.anonymize("823003113189049"),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize("100064878993116"),
            normalisers.anonymize("100064878993116"),
            normalisers.anonymize("100064878993116"),
            normalisers.anonymize("100064381045972"),
            normalisers.anonymize("100064381045972"),
            normalisers.anonymize("100064381045972"),
            normalisers.anonymize("100064878993116"),
            normalisers.anonymize("100064381045972"),
        ],
        "phoenix_platform_parent_message_id": [None, None, None, None, None, None, None, None],
    }

    df = pd.DataFrame(data)  # noqa: PD901
    df["gather_id"] = 1
    df["gather_batch_id"] = 3
    df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    df["source"] = schemas.Source.apify
    df["platform"] = schemas.Platform.facebook
    df["data_type"] = schemas.DataType.posts
    df["phoenix_processed_at"] = datetime.fromisoformat("2024-04-02T12:10:59.000Z")
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        df[column] = df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]

    return df


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normalise_batch(expected_dataframe, facebook_posts_gather_fixture):
    """Test normalise_batch function."""
    batch_json = utils.load_sample_raw_data(
        source=schemas.Source.apify,
        platform=schemas.Platform.facebook,
        data_type=schemas.DataType.posts,
    )

    processed_df = normalisers.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_posts_json,
        batch_json=batch_json,
        gather=facebook_posts_gather_fixture,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )

    pd.testing.assert_frame_equal(processed_df, expected_dataframe)
    assert processed_df["source"].iloc[0] == "apify"


@pytest.mark.patch_settings(
    {
        "USE_MOCK_APIFY": True,
        "USE_MOCK_BQ": True,
        "APIFY_API_KEYS": {"main": "dummy_key"},
    }
)
def test_normalise_batches(
    tmpdir, patch_settings, mocker, facebook_posts_gather_fixture, expected_dataframe, freezer
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
        normalisers.normalise_batches.fn(
            gather=facebook_posts_gather_fixture,
            job_run_id=1,
            bigquery_dataset="test_dataset",
        )

    # Check that the normalized data was written to the correct Parquet file
    parquet_file_path = tmpdir.join("test_dataset", "generalised_messages.parquet")
    assert parquet_file_path.check()

    # Alter expected DataFrame to match that now using multiple batches
    expected_dataframe["gather_batch_id"] = [0, 0, 0, 1, 1, 1, 2, 2]

    # Load the parquet file and verify its contents
    processed_df = pd.read_parquet(parquet_file_path)
    pd.testing.assert_frame_equal(processed_df, expected_dataframe)
    assert processed_df["source"].iloc[0] == "apify"
