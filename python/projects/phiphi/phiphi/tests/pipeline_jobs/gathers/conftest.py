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
def facebook_search_posts_gather_fixture() -> (
    gathers.apify_facebook_search_posts.schemas.ApifyFacebookSearchPostsGatherResponse
):
    """Fixture for the Facebook search posts gather example."""
    return example_gathers.facebook_search_posts_gather_example()


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
def tiktok_searches_posts_gather_fixture() -> (
    gathers.apify_tiktok_searches_posts.schemas.ApifyTikTokSearchesPostsGatherResponse
):
    """Fixture for the TikTok searches posts gather example."""
    return example_gathers.tiktok_searches_posts_gather_example()


@pytest.fixture
def tiktok_comments_gather_fixture() -> (
    gathers.apify_tiktok_comments.schemas.ApifyTikTokCommentsGatherResponse
):
    """Fixture for the TikTok comments gather example."""
    return example_gathers.tiktok_comments_gather_example()


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
        "like_count": [4, 3, 2, 477, 1259, 956, 3, 2327],
        "share_count": [1, 3, 0, 171, 261, 347, 1, 1054],
        "comment_count": [0, 0, 0, 203, 229, 388, 0, 214],
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
def normalised_facebook_search_posts_df() -> pd.DataFrame:
    """Return the expected DataFrame based on the processed JSON data."""
    data = {
        "pi_platform_message_id": [
            "facebook_search_posts-postId1",
            "facebook_search_posts-postId2",
            "facebook_search_posts-postId3",
            "facebook_search_posts-postId4",
        ],
        "pi_platform_message_author_id": [
            "facebook_search_posts-authorID1",
            "facebook_search_posts-authorID2",
            "facebook_search_posts-authorID3",
            "facebook_search_posts-authorID4",
        ],
        "pi_platform_message_author_name": [
            "facebook_search_posts-authorName1",
            "facebook_search_posts-authorName2",
            "facebook_search_posts-authorName3",
            "facebook_search_posts-authorName4",
        ],
        "pi_platform_parent_message_id": [None] * 4,
        "pi_platform_root_message_id": [None] * 4,
        "pi_text": [
            "ONE MORE HELLO OR ONE LAST GOODBYE! \\ud83d",
            "One more hello or one last goodbye? \\n\\nWitness their new world.",
            "test",
            "One more hello or one last goodbye? \\u2708\\ufe0f",
        ],
        "pi_platform_message_url": [
            "https://www.facebook.com/authorId1/posts/urlId1",
            "https://www.facebook.com/authorId2/videos/urlId2",
            "https://www.facebook.com/authorId3/videos/urlId3",
            "https://www.facebook.com/authorId4/videos/urlId4",
        ],
        "platform_message_last_updated_at": [
            datetime.utcfromtimestamp(1728388135),
            datetime.utcfromtimestamp(1728387357),
            datetime.utcfromtimestamp(1728385343),
            datetime.utcfromtimestamp(1728387354),
        ],
        "phoenix_platform_message_id": [
            normalisers.anonymize("facebook_search_posts-postId1"),
            normalisers.anonymize("facebook_search_posts-postId2"),
            normalisers.anonymize("facebook_search_posts-postId3"),
            normalisers.anonymize("facebook_search_posts-postId4"),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize("facebook_search_posts-authorID1"),
            normalisers.anonymize("facebook_search_posts-authorID2"),
            normalisers.anonymize("facebook_search_posts-authorID3"),
            normalisers.anonymize("facebook_search_posts-authorID4"),
        ],
        "phoenix_platform_parent_message_id": [None] * 4,
        "phoenix_platform_root_message_id": [None] * 4,
        "like_count": [91, 125, 3, 36],
        "share_count": [0] * 4,
        "comment_count": [15, 43, 0, 3],
    }

    df = pd.DataFrame(data)  # noqa: PD901
    df["gather_id"] = 7
    df["gather_batch_id"] = 3
    df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    df["gather_type"] = gathers.schemas.ChildTypeName.apify_facebook_search_posts.value
    df["platform"] = gathers.schemas.Platform.facebook
    df["data_type"] = gathers.schemas.DataType.posts
    df["phoenix_processed_at"] = datetime.fromisoformat("2024-04-02T12:10:59.000Z")
    # For some reason UTC is not typed correctly in pandas but is in the normalisation.
    df["platform_message_last_updated_at"] = df["platform_message_last_updated_at"].dt.tz_localize(
        "UTC"
    )
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
            # No "text" key in blob is for comment that are images. We include them but with empty
            # text
            "",
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
        "like_count": [4, 2, 2, 1, 1, 1, 0, 2, 1],
        "share_count": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "comment_count": [1, 3, 2, 0, 0, 2, 0, 5, 0],
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
            "tiktok-accounts-id1",
            "tiktok-accounts-id2",
            "tiktok-accounts-id3",
        ],
        "pi_platform_message_author_id": [
            "tiktok-accounts-authorMetaId1",
            "tiktok-accounts-authorMetaId2",
            "tiktok-accounts-authorMetaId3",
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
            normalisers.anonymize("tiktok-accounts-id1"),
            normalisers.anonymize("tiktok-accounts-id2"),
            normalisers.anonymize("tiktok-accounts-id3"),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize("tiktok-accounts-authorMetaId1"),
            normalisers.anonymize("tiktok-accounts-authorMetaId2"),
            normalisers.anonymize("tiktok-accounts-authorMetaId3"),
        ],
        "phoenix_platform_parent_message_id": [None, None, None],
        "phoenix_platform_root_message_id": [None, None, None],
        "like_count": [2268, 6804, 1314],
        "share_count": [636, 244, 11],
        "comment_count": [174, 232, 65],
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


@pytest.fixture
def normalised_tiktok_searches_posts_df() -> pd.DataFrame:
    """Return the expected DataFrame based on the processed JSON data."""
    data = {
        "pi_platform_message_id": [
            "tiktok-searches-id1",
            "tiktok-searches-id2",
            "tiktok-searches-id3",
            "tiktok-searches-id4",
            "tiktok-searches-id5",
            "tiktok-searches-id6",
        ],
        "pi_platform_message_author_id": [
            "tiktok-searches-authorMetaId1",
            "tiktok-searches-authorMetaId2",
            "tiktok-searches-authorMetaId3",
            "tiktok-searches-authorMetaId4",
            "tiktok-searches-authorMetaId5",
            "tiktok-searches-authorMetaId6",
        ],
        "pi_platform_message_author_name": [
            "tiktok-searches-authorMetaName1",
            "tiktok-searches-authorMetaName2",
            "tiktok-searches-authorMetaName3",
            "tiktok-searches-authorMetaName4",
            "tiktok-searches-authorMetaName5",
            "tiktok-searches-authorMetaName6",
        ],
        "pi_platform_parent_message_id": [None] * 6,
        "pi_platform_root_message_id": [None] * 6,
        "pi_text": [
            "Finding peace often requires letting go of people",
            "You find peace in the countryside #countrysidelife",
            "for my birthday I want PEACE and NO human interaction",
            "Hello World #programming #coding #python #codingmemes ",
            "#helloworld #painisanillusion #fyp I am a trained martial arts practitioner",
            "text6",
        ],
        "pi_platform_message_url": [
            "https://www.tiktok.com/@tiktok-searches-authorMetaProfileUrl1/video/id1",
            "https://www.tiktok.com/@tiktok-searches-authorMetaProfileUrl2/video/id2",
            "https://www.tiktok.com/@tiktok-searches-authorMetaProfileUrl3/video/id3",
            "https://www.tiktok.com/@tiktok-searches-authorMetaProfileUrl4/video/id4",
            "https://www.tiktok.com/@tiktok-searches-authorMetaProfileUrl5/video/id5",
            "https://www.tiktok.com/@tiktok-searches-authorMetaProfileUrl6/video/id6",
        ],
        "platform_message_last_updated_at": [
            1676503649000,
            1715610890000,
            1721064158000,
            1725019495000,
            1723029970000,
            1725793230000,
        ],
        "phoenix_platform_message_id": [
            normalisers.anonymize("tiktok-searches-id1"),
            normalisers.anonymize("tiktok-searches-id2"),
            normalisers.anonymize("tiktok-searches-id3"),
            normalisers.anonymize("tiktok-searches-id4"),
            normalisers.anonymize("tiktok-searches-id5"),
            normalisers.anonymize("tiktok-searches-id6"),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize("tiktok-searches-authorMetaId1"),
            normalisers.anonymize("tiktok-searches-authorMetaId2"),
            normalisers.anonymize("tiktok-searches-authorMetaId3"),
            normalisers.anonymize("tiktok-searches-authorMetaId4"),
            normalisers.anonymize("tiktok-searches-authorMetaId5"),
            normalisers.anonymize("tiktok-searches-authorMetaId6"),
        ],
        "phoenix_platform_parent_message_id": [None] * 6,
        "phoenix_platform_root_message_id": [None] * 6,
        "like_count": [54100, 469900, 105500, 491200, 0, 0],
        "share_count": [11800, 15200, 3500, 77300, 0, 0],
        "comment_count": [304, 2197, 900, 4112, 2496, 0],
    }
    normalised_tiktok_df = pd.DataFrame(data)
    normalised_tiktok_df["gather_id"] = 6
    normalised_tiktok_df["gather_batch_id"] = 3
    normalised_tiktok_df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    normalised_tiktok_df[
        "gather_type"
    ] = gathers.schemas.ChildTypeName.apify_tiktok_searches_posts.value
    normalised_tiktok_df["platform"] = gathers.schemas.Platform.tiktok
    normalised_tiktok_df["data_type"] = gathers.schemas.DataType.posts
    normalised_tiktok_df["phoenix_processed_at"] = datetime.fromisoformat(
        "2024-04-02T12:10:59.000Z"
    )
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        normalised_tiktok_df[column] = normalised_tiktok_df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]

    return normalised_tiktok_df


@pytest.fixture
def normalised_tiktok_hashtags_posts_df() -> pd.DataFrame:
    """Return the expected DataFrame based on the processed JSON data."""
    data = {
        "pi_platform_message_id": [
            "tiktok-hashtags-id1",
            "tiktok-hashtags-id2",
            "tiktok-hashtags-id3",
            "tiktok-hashtags-id4",
            "tiktok-hashtags-id5",
            "tiktok-hashtags-id6",
        ],
        "pi_platform_message_author_id": [
            "tiktok-hashtags-authorMetaId1",
            "tiktok-hashtags-authorMetaId2",
            "tiktok-hashtags-authorMetaId3",
            "tiktok-hashtags-authorMetaId4",
            "tiktok-hashtags-authorMetaId5",
            "tiktok-hashtags-authorMetaId6",
        ],
        "pi_platform_message_author_name": [
            "bbcnews",
            "bbcnews",
            "bbcnews",
            "authorMetaName4",
            "unitednations",
            "cbsnews",
        ],
        "pi_platform_parent_message_id": [None] * 6,
        "pi_platform_root_message_id": [None] * 6,
        "pi_text": [
            "There's still time to see it! #BBCNews",
            "At the Democratic National Convention",
            "A major crackdown on smokers and vapers #BBCNews",
            "The #unitednations #knowledge",
            "The war in #Sudan has displaced 10 million people. #UnitedNations",
            "President Biden tells the U.N. #news #biden #unitednations ",
        ],
        "pi_platform_message_url": [
            "https://www.tiktok.com/@bbcnews/video/webVideoUrl1",
            "https://www.tiktok.com/@bbcnews/video/webVideoUrl2",
            "https://www.tiktok.com/@bbcnews/video/webVideoUrl3",
            "https://www.tiktok.com/@authorMetaName4/video/webVideoUrl4",
            "https://www.tiktok.com/@unitednations/video/webVideoUrl5",
            "https://www.tiktok.com/@cbsnews/video/webVideoUrl6",
        ],
        "platform_message_last_updated_at": [
            1724086800000,
            1724219490000,
            1721216700000,
            1716304501000,
            1721748028000,
            1663784721000,
        ],
        "phoenix_platform_message_id": [
            normalisers.anonymize("tiktok-hashtags-id1"),
            normalisers.anonymize("tiktok-hashtags-id2"),
            normalisers.anonymize("tiktok-hashtags-id3"),
            normalisers.anonymize("tiktok-hashtags-id4"),
            normalisers.anonymize("tiktok-hashtags-id5"),
            normalisers.anonymize("tiktok-hashtags-id6"),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize("tiktok-hashtags-authorMetaId1"),
            normalisers.anonymize("tiktok-hashtags-authorMetaId2"),
            normalisers.anonymize("tiktok-hashtags-authorMetaId3"),
            normalisers.anonymize("tiktok-hashtags-authorMetaId4"),
            normalisers.anonymize("tiktok-hashtags-authorMetaId5"),
            normalisers.anonymize("tiktok-hashtags-authorMetaId6"),
        ],
        "phoenix_platform_parent_message_id": [None] * 6,
        "phoenix_platform_root_message_id": [None] * 6,
        "like_count": [137800, 4955, 211900, 6845, 729, 674900],
        "share_count": [16200, 152, 24000, 542, 46, 12600],
        "comment_count": [1167, 181, 7705, 0, 485, 18100],
    }
    normalised_tiktok_df = pd.DataFrame(data)
    normalised_tiktok_df["gather_id"] = 4
    normalised_tiktok_df["gather_batch_id"] = 3
    normalised_tiktok_df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    normalised_tiktok_df[
        "gather_type"
    ] = gathers.schemas.ChildTypeName.apify_tiktok_hashtags_posts.value
    normalised_tiktok_df["platform"] = gathers.schemas.Platform.tiktok
    normalised_tiktok_df["data_type"] = gathers.schemas.DataType.posts
    normalised_tiktok_df["phoenix_processed_at"] = datetime.fromisoformat(
        "2024-04-02T12:10:59.000Z"
    )
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        normalised_tiktok_df[column] = normalised_tiktok_df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]

    return normalised_tiktok_df


@pytest.fixture
def normalised_tiktok_comments_df() -> pd.DataFrame:
    """Return the expected DataFrame based on the processed JSON data."""
    data = {
        "pi_platform_message_id": [
            "anonymizedID1",
            "anonymizedID2",
            "anonymizedID3",
            "anonymizedID4",
        ],
        "pi_platform_message_author_id": [
            "anonymizedUserID1",
            "anonymizedUserID2",
            "anonymizedUserID3",
            "anonymizedUserID4",
        ],
        "pi_platform_message_author_name": [
            "anonymizedUsername1",
            "anonymizedUsername2",
            "anonymizedUsername3",
            "anonymizedUsername4",
        ],
        "pi_platform_parent_message_id": [
            "anonymizedAwemeID1",
            "anonymizedAwemeID2",
            "anonymizedAwemeID3",
            "anonymizedParentID4",
        ],
        "pi_platform_root_message_id": [
            "anonymizedAwemeID1",
            "anonymizedAwemeID2",
            "anonymizedAwemeID3",
            "anonymizedAwemeID4",
        ],
        "pi_text": [
            (
                "please help save [country's] water bodies. "
                "they are being destroyed by illegal mining activities"
            ),
            "",
            "[International organization], please take care of the foreigners in [country]",
            "womp womp",
        ],
        "pi_platform_message_url": [None] * 4,
        "platform_message_last_updated_at": [
            datetime.fromisoformat("2024-09-09T18:40:45.000Z"),
            datetime.fromisoformat("2024-09-10T06:29:28.000Z"),
            datetime.fromisoformat("2024-09-09T23:46:51.000Z"),
            datetime.fromisoformat("2024-06-02T07:09:12.000Z"),
        ],
        "phoenix_platform_message_id": [
            normalisers.anonymize("anonymizedID1"),
            normalisers.anonymize("anonymizedID2"),
            normalisers.anonymize("anonymizedID3"),
            normalisers.anonymize("anonymizedID4"),
        ],
        "phoenix_platform_message_author_id": [
            normalisers.anonymize("anonymizedUserID1"),
            normalisers.anonymize("anonymizedUserID2"),
            normalisers.anonymize("anonymizedUserID3"),
            normalisers.anonymize("anonymizedUserID4"),
        ],
        "phoenix_platform_parent_message_id": [
            normalisers.anonymize("anonymizedAwemeID1"),
            normalisers.anonymize("anonymizedAwemeID2"),
            normalisers.anonymize("anonymizedAwemeID3"),
            normalisers.anonymize("anonymizedParentID4"),
        ],
        "phoenix_platform_root_message_id": [
            normalisers.anonymize("anonymizedAwemeID1"),
            normalisers.anonymize("anonymizedAwemeID2"),
            normalisers.anonymize("anonymizedAwemeID3"),
            normalisers.anonymize("anonymizedAwemeID4"),
        ],
        "like_count": [0, 0, 0, 3],
        "share_count": [0, 0, 0, 0],
        "comment_count": [1, 0, 0, 0],
    }
    normalised_tiktok_df = pd.DataFrame(data)
    normalised_tiktok_df["gather_id"] = 5
    normalised_tiktok_df["gather_batch_id"] = 3
    normalised_tiktok_df["gathered_at"] = pd.to_datetime("2024-04-01T12:00:00.000Z")
    normalised_tiktok_df["gather_type"] = gathers.schemas.ChildTypeName.apify_tiktok_comments.value
    normalised_tiktok_df["platform"] = gathers.schemas.Platform.tiktok
    normalised_tiktok_df["data_type"] = gathers.schemas.DataType.comments
    normalised_tiktok_df["phoenix_processed_at"] = datetime.fromisoformat(
        "2024-04-02T12:10:59.000Z"
    )
    for column in ["platform_message_last_updated_at", "gathered_at", "phoenix_processed_at"]:
        normalised_tiktok_df[column] = normalised_tiktok_df[column].astype("datetime64[ms, UTC]")  # type: ignore[call-overload]
    return normalised_tiktok_df
