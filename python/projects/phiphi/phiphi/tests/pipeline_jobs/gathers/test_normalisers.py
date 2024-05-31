"""Tests for the normalisers module."""
from datetime import datetime

import pandas as pd
import pytest

from phiphi.api.projects.gathers import schemas
from phiphi.pipeline_jobs.gathers import normalisers, utils


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
            datetime.fromisoformat("2024-04-03T06:00:25"),
            datetime.fromisoformat("2024-03-25T07:00:17"),
            datetime.fromisoformat("2024-02-22T16:00:01"),
            datetime.fromisoformat("2024-04-03T18:02:22"),
            datetime.fromisoformat("2024-04-03T08:02:00"),
            datetime.fromisoformat("2024-04-02T18:04:00"),
            datetime.fromisoformat("2024-02-21T08:00:10"),
            datetime.fromisoformat("2024-04-02T08:07:30"),
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
    df["project_id"] = 1
    df["gather_id"] = 2
    df["gather_batch_id"] = 3
    df["gathered_at"] = datetime.fromisoformat("2024-04-01T12:00:00")
    df["source"] = schemas.Source.apify
    df["platform"] = schemas.Platform.facebook
    df["data_type"] = schemas.DataType.posts
    df["phoenix_processed_at"] = datetime.fromisoformat("2024-04-02T12:10:59")

    return df


@pytest.mark.freeze_time(datetime.fromisoformat("2024-04-02T12:10:59"))
def test_normalise_batch(expected_dataframe):
    """Test normalise_batch function."""
    batch_json = utils.load_sample_raw_data(
        source=schemas.Source.apify,
        platform=schemas.Platform.facebook,
        data_type=schemas.DataType.posts,
    )

    processed_df = normalisers.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_posts_json,
        batch_json=batch_json,
        project_id=1,
        gather_id=2,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00"),
        source=schemas.Source.apify,
        platform=schemas.Platform.facebook,
        data_type=schemas.DataType.posts,
    )

    pd.testing.assert_frame_equal(processed_df, expected_dataframe)
    assert processed_df["source"].iloc[0] == "apify"
