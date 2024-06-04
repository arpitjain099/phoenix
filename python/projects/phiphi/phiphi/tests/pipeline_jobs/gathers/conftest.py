"""Conftest for tests for the gather pipeline job."""
from datetime import datetime

import pandas as pd
import pytest

from phiphi.api.projects import gathers
from phiphi.pipeline_jobs.gathers import normalisers
from phiphi.tests.pipeline_jobs.gathers import example_gathers


@pytest.fixture
def facebook_posts_gather_fixture() -> (
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse
):
    """Fixture for the Facebook posts gather example."""
    return example_gathers.facebook_posts_gather_example()


@pytest.fixture
def facebook_comments_gather_fixture() -> (
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse
):
    """Fixture for the Facebook comments gather example."""
    return example_gathers.facebook_comments_gather_example()


@pytest.fixture
def normalised_facebook_posts_df() -> pd.DataFrame:
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
    df["source"] = gathers.schemas.Source.apify
    df["platform"] = gathers.schemas.Platform.facebook
    df["data_type"] = gathers.schemas.DataType.posts
    df["phoenix_processed_at"] = datetime.fromisoformat("2024-04-02T12:10:59.000Z")
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        df[column] = df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]

    return df
