"""Conftest for tests for the gather pipeline job."""
from datetime import datetime

import pandas as pd
import pytest

from phiphi.api.projects import gathers
from phiphi.pipeline_jobs.gathers import normalisers
from phiphi.tests.pipeline_jobs.gathers import example_gathers


@pytest.fixture
def facebook_posts_gather_fixture() -> (
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse
):
    """Fixture for the Facebook posts gather example."""
    return example_gathers.facebook_posts_gather_example()


@pytest.fixture
def facebook_comments_gather_fixture() -> (
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentsGatherResponse
):
    """Fixture for the Facebook comments gather example."""
    return example_gathers.facebook_comments_gather_example()


@pytest.fixture
def tiktok_accounts_posts_gather_fixture() -> (
    gathers.apify_tiktok_accounts_posts.schemas.ApifyTikTokAccountsPostsGatherResponse
):
    """Fixture for the TikTok accounts posts gather example."""
    return example_gathers.tiktok_accounts_posts_gather_example()


@pytest.fixture
def tiktok_hashtags_posts_gather_fixture() -> (
    gathers.apify_tiktok_hashtags_posts.schemas.ApifyTikTokHashtagsPostsGatherResponse
):
    """Fixture for the TikTok hashtags posts gather example."""
    return example_gathers.tiktok_hashtags_posts_gather_example()


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
        "pi_platform_root_message_id": [None, None, None, None, None, None, None, None],
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
        "phoenix_platform_root_message_id": [None, None, None, None, None, None, None, None],
    }

    df = pd.DataFrame(data)  # noqa: PD901
    df["gather_id"] = 1
    df["gather_batch_id"] = 3
    df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    df["gather_type"] = gathers.schemas.ChildTypeName.apify_facebook_posts.value
    df["platform"] = gathers.schemas.Platform.facebook
    df["data_type"] = gathers.schemas.DataType.posts
    df["phoenix_processed_at"] = datetime.fromisoformat("2024-04-02T12:10:59.000Z")
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        df[column] = df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]

    return df


@pytest.fixture
def normalised_facebook_comments_df() -> pd.DataFrame:
    """Return the expected DataFrame based on the processed JSON data."""
    data = {
        "pi_platform_message_id": [
            "Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfOTYxNjQ3MDc4ODA5NzM1",
            "Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfNzcyNTQ5MjA4MTc0NjM4",
            "Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfOTQyNjY5MDc0MTkwNTIz",
            "Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfMTUyMDM5OTc0ODU5MzY2NA==",
            "Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfNzI1MjA5MDE2NDMyMjAz",
            "Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfNzI4NTI5NDQ2ODE4NTgxOA==",
            "Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfMTM1Njc3Njg4NDk5NzU1Mg==",
            "Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfMTEzNzU1NDU2NDE2MjcwMQ==",
            "Y29tbWVudDo3NjM3MTY1OTE5NjYwMzMyXzQyNjU5NzcyOTk5MDI2OA==",
        ],
        "pi_platform_message_author_id": [
            "pfbid02CWk7wdftZWU4ChNjeqbvkd6ePFh8YrDTv5mMuqV7hzRNy7cq6TzDyDnSe4SaK87Xl",
            "100024915288912",
            "pfbid0M9N6BtGwe2g76dEPzMAsmRa4xUowvx8ohdMHbqHgCfssWyap6Gyr6RueezmvZeXml",
            "pfbid02n7VKGoXEYpLj5vMDb8QCk2ZY7wbqqudAz25ftbqGwTm7D5vKPWw8qNtHwy5mqBiql",
            "100087182205819",
            "pfbid0aZ3q95k4ZMWH6T3XSSJybx5kLrSCXRW9ZFRoxyQT7ji1xsM9UL5LECHqdyKoEUzql",
            "100063654872822",
            "pfbid0txFVuZ1ib4vwyB1ieojzyWZ8DoWtG6sR2W8dHP6EHZ5Gmw2TBz4bVk1fiAxdbeKYl",
            "pfbid02wia9a2GDCRqQH2aSty35ZBwNMHZpys2UajNSYaW1sKLxNxw22Ebc1Vk64KusqWnxl",
        ],
        "pi_platform_message_author_name": [
            "Binu Pg",
            "Sally Yuan",
            "Jamil Mohammad",
            "Judy Haila",
            "एक युद्ध पाखंडवाद व अंधविश्वास के खिलाफ",
            "Ashraf Rahman",
            "Rex Omolleh Nairobi West Ward MCA.",
            "Cynthia Keels",
            "Bah Rahman Bouba",
        ],
        "pi_platform_parent_message_id": [
            "823689576453736",
            "823689576453736",
            "823689576453736",
            "823689576453736",
            "823003113189049",
            "823003113189049",
            "823003113189049",
            "823003113189049",
            "Y29tbWVudDo3NjM3MTY1OTE5NjYwMzMyXzc5MTgyMjgxMTQ4OTUwNDY=",
        ],
        "pi_platform_root_message_id": [
            "823689576453736",
            "823689576453736",
            "823689576453736",
            "823689576453736",
            "823003113189049",
            "823003113189049",
            "823003113189049",
            "823003113189049",
            "7637165919660332",
        ],
        "pi_text": [
            "Birthday wishes Dr.Jane Goodall. world.",
            "Happy birthday",
            "Best wishes of Happy Birthday",
            "Happy Birthday. Thank you for doing what you do to make our planet a better place.",
            "The main goal of all of us should be to build a.",
            "Thanks a lot to all of you do for huminity👍❤️",
            "Awesome 👏 \nHappy autism day",
            "and thank you lord and thank you God Amen",
            "Le PMU c'est pour qui ?😄😄😄",
        ],
        "pi_platform_message_url": [
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl?comment_id=961647078809735",
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl?comment_id=772549208174638",
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl?comment_id=942669074190523",
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl?comment_id=1520399748593664",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml?comment_id=725209016432203",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml?comment_id=7285294468185818",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml?comment_id=1356776884997552",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml?comment_id=1137554564162701",
            "https://www.facebook.com/malick.konate.56/posts/7637165919660332?comment_id=426597729990268",
        ],
        "platform_message_last_updated_at": [
            datetime.fromisoformat("2024-04-03T08:58:38.000Z"),
            datetime.fromisoformat("2024-04-03T10:59:05.000Z"),
            datetime.fromisoformat("2024-04-03T09:03:29.000Z"),
            datetime.fromisoformat("2024-04-03T17:47:58.000Z"),
            datetime.fromisoformat("2024-04-03T04:56:01.000Z"),
            datetime.fromisoformat("2024-04-02T15:21:12.000Z"),
            datetime.fromisoformat("2024-04-02T09:04:43.000Z"),
            datetime.fromisoformat("2024-04-02T10:59:46.000Z"),
            datetime.fromisoformat("2024-04-22T19:12:51.000Z"),
        ],
        "phoenix_platform_message_id": [
            normalisers.anonymize("Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfOTYxNjQ3MDc4ODA5NzM1"),
            normalisers.anonymize("Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfNzcyNTQ5MjA4MTc0NjM4"),
            normalisers.anonymize("Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfOTQyNjY5MDc0MTkwNTIz"),
            normalisers.anonymize("Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfMTUyMDM5OTc0ODU5MzY2NA=="),
            normalisers.anonymize("Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfNzI1MjA5MDE2NDMyMjAz"),
            normalisers.anonymize("Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfNzI4NTI5NDQ2ODE4NTgxOA=="),
            normalisers.anonymize("Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfMTM1Njc3Njg4NDk5NzU1Mg=="),
            normalisers.anonymize("Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfMTEzNzU1NDU2NDE2MjcwMQ=="),
            normalisers.anonymize("Y29tbWVudDo3NjM3MTY1OTE5NjYwMzMyXzQyNjU5NzcyOTk5MDI2OA=="),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize(
                "pfbid02CWk7wdftZWU4ChNjeqbvkd6ePFh8YrDTv5mMuqV7hzRNy7cq6TzDyDnSe4SaK87Xl"
            ),
            normalisers.anonymize("100024915288912"),
            normalisers.anonymize(
                "pfbid0M9N6BtGwe2g76dEPzMAsmRa4xUowvx8ohdMHbqHgCfssWyap6Gyr6RueezmvZeXml"
            ),
            normalisers.anonymize(
                "pfbid02n7VKGoXEYpLj5vMDb8QCk2ZY7wbqqudAz25ftbqGwTm7D5vKPWw8qNtHwy5mqBiql"
            ),
            normalisers.anonymize("100087182205819"),
            normalisers.anonymize(
                "pfbid0aZ3q95k4ZMWH6T3XSSJybx5kLrSCXRW9ZFRoxyQT7ji1xsM9UL5LECHqdyKoEUzql"
            ),
            normalisers.anonymize("100063654872822"),
            normalisers.anonymize(
                "pfbid0txFVuZ1ib4vwyB1ieojzyWZ8DoWtG6sR2W8dHP6EHZ5Gmw2TBz4bVk1fiAxdbeKYl"
            ),
            normalisers.anonymize(
                "pfbid02wia9a2GDCRqQH2aSty35ZBwNMHZpys2UajNSYaW1sKLxNxw22Ebc1Vk64KusqWnxl"
            ),
        ],
        "phoenix_platform_parent_message_id": [
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("Y29tbWVudDo3NjM3MTY1OTE5NjYwMzMyXzc5MTgyMjgxMTQ4OTUwNDY="),
        ],
        "phoenix_platform_root_message_id": [
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823689576453736"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("823003113189049"),
            normalisers.anonymize("7637165919660332"),
        ],
    }

    df = pd.DataFrame(data)  # noqa: PD901
    df["gather_id"] = 2
    df["gather_batch_id"] = 3
    df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    df["gather_type"] = gathers.schemas.ChildTypeName.apify_facebook_comments.value
    df["platform"] = gathers.schemas.Platform.facebook
    df["data_type"] = gathers.schemas.DataType.comments
    df["phoenix_processed_at"] = datetime.fromisoformat("2024-04-02T12:10:59.000Z")
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        df[column] = df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]

    return df


@pytest.fixture
def normalised_tiktok_accounts_posts_df() -> pd.DataFrame:
    """Return the expected DataFrame based on the processed JSON data."""
    data = {
        "pi_platform_message_id": [
            "id1",
            "id2",
            "id3",
        ],
        "pi_platform_message_author_id": [
            "authorMetaId1",
            "authorMetaId2",
            "authorMetaId3",
        ],
        "pi_platform_message_author_name": ["bbcnews", "bbcnews", "bbcnews"],
        "pi_platform_parent_message_id": [None, None, None],
        "pi_platform_root_message_id": [None, None, None],
        "pi_text": [
            "US President Joe Biden mistakenly referred ... \\u201cPresident Putin\\u201d ...",
            "... the son of Asia\\'s richest man, ... \\u00a0#India #Mumbai #IndianWedding ...",
            "Do you think a deal can be made? #JuniorDoctors #JuniorDoctorStrikes #WesStreeting",
        ],
        "pi_platform_message_url": [
            "https://www.tiktok.com/@bbcnews/video/webVideoUrl1",
            "https://www.tiktok.com/@bbcnews/video/webVideoUrl2",
            "https://www.tiktok.com/@bbcnews/video/webVideoUrl3",
        ],
        "platform_message_last_updated_at": [1720741311000, 1720731600000, 1720729800000],
        "phoenix_platform_message_id": [
            normalisers.anonymize("id1"),
            normalisers.anonymize("id2"),
            normalisers.anonymize("id3"),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize("authorMetaId1"),
            normalisers.anonymize("authorMetaId2"),
            normalisers.anonymize("authorMetaId3"),
        ],
        "phoenix_platform_parent_message_id": [None, None, None],
        "phoenix_platform_root_message_id": [None, None, None],
    }
    normalised_tiktok_df = pd.DataFrame(data)
    normalised_tiktok_df["gather_id"] = 3
    normalised_tiktok_df["gather_batch_id"] = 3
    normalised_tiktok_df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    normalised_tiktok_df[
        "gather_type"
    ] = gathers.schemas.ChildTypeName.apify_tiktok_accounts_posts.value
    normalised_tiktok_df["platform"] = gathers.schemas.Platform.tiktok
    normalised_tiktok_df["data_type"] = gathers.schemas.DataType.posts
    normalised_tiktok_df["phoenix_processed_at"] = datetime.fromisoformat(
        "2024-04-02T12:10:59.000Z"
    )
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        normalised_tiktok_df[column] = normalised_tiktok_df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]

    return normalised_tiktok_df
