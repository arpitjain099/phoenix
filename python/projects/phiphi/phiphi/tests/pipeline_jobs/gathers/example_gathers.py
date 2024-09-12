"""Example gathers (reponses/rows/specs)."""
import datetime

from phiphi.api.projects import gathers


def facebook_posts_gather_example() -> (
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse
):
    """Example for ApifyFacebookPostsGatherResponse schema."""
    return gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse(
        name="Example",
        limit_posts_per_account=4,
        account_url_list=[
            "https://www.facebook.com/howtobuildup/",
            "https://www.facebook.com/unitednations/",
        ],
        posts_created_after="2024-01-03",
        posts_created_before="2024-04-04",
        id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_posts,
    )


def facebook_comments_gather_example() -> (
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentsGatherResponse
):
    """Example for ApifyFacebookCommentsGatherResponse schema."""
    return gathers.apify_facebook_comments.schemas.ApifyFacebookCommentsGatherResponse(
        name="Example",
        limit_comments_per_post=4,
        post_url_list=[
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml",
        ],
        sort_comments_by=gathers.apify_facebook_comments.schemas.FacebookCommentSortOption.facebook_default,
        include_comment_replies=False,
        id=2,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_comments,
    )


def tiktok_accounts_posts_gather_example() -> (
    gathers.apify_tiktok_accounts_posts.schemas.ApifyTikTokAccountsPostsGatherResponse
):
    """Example for ApifyTiktokAccountsPostsGatherResponse schema."""
    return gathers.apify_tiktok_accounts_posts.schemas.ApifyTikTokAccountsPostsGatherResponse(
        name="Example",
        account_username_list=["@unitednations", "@bbcnews"],
        limit_posts_per_account=3,
        id=3,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_accounts_posts,
    )


def tiktok_hashtags_posts_gather_example() -> (
    gathers.apify_tiktok_hashtags_posts.schemas.ApifyTikTokHashtagsPostsGatherResponse
):
    """Example for ApifyTiktokHashtagsGatherPostsResponse schema."""
    return gathers.apify_tiktok_hashtags_posts.schemas.ApifyTikTokHashtagsPostsGatherResponse(
        name="Example",
        hashtag_list=["unitednations", "bbcnews"],
        limit_posts_per_hashtag=3,
        id=4,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_hashtags_posts,
    )


def tiktok_comments_gather_example() -> (
    gathers.apify_tiktok_comments.schemas.ApifyTikTokCommentsGatherResponse
):
    """Example for ApifyTiktokCommentsGatherResponse schema."""
    return gathers.apify_tiktok_comments.schemas.ApifyTikTokCommentsGatherResponse(
        name="Example",
        post_url_list=[
            # These are real URLs but from public organisations
            "https://www.tiktok.com/@unitednations/video/7412700631284141355",
            "https://www.tiktok.com/@bbc/video/7413716097670630689",
        ],
        limit_comments_per_post=3,
        include_comment_replies=True,
        id=5,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_comments,
    )
