"""Example gathers (reponses/rows/specs)."""
import datetime

from phiphi.api.projects import gathers


def facebook_posts_gather_example() -> (
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse
):
    """Example for ApifyFacebookPostGatherResponse schema."""
    return gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse(
        name="Example",
        limit_posts_per_account=4,
        account_url_list=[
            "https://www.facebook.com/howtobuildup/",
            "https://www.facebook.com/unitednations/",
        ],
        posts_created_after="2024-04-04",
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
        child_type=gathers.schemas.ChildTypeName.apify_facebook_posts,
    )


def facebook_comments_gather_example() -> (
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse
):
    """Example for ApifyFacebookCommentGatherResponse schema."""
    return gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse(
        name="Example",
        limit_comments_per_post=4,
        post_url_list=[
            "https://www.facebook.com/unitednations/posts/pfbid045as8QKV2uLVYe2NumDPs7a68Hr4P5cjmoyMRo2e4dj4p3rp2gWNNj948Uu7BVcxl",
            "https://www.facebook.com/unitednations/posts/pfbid0LmBjLodaYjFhvntY3rX4xB2cyrcUeXHuasXJNFgimkNX7NE76CjSEYCwwveF9v5ml",
        ],
        sort_comments_by=gathers.apify_facebook_comments.schemas.FacebookCommentSortOption.facebook_default,
        include_comment_replies=False,
        id=2,
        platform=gathers.schemas.Platform.facebook,
        data_type=gathers.schemas.DataType.comments,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        deleted_at=None,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_facebook_comments,
    )


def tiktok_accounts_posts_gather_example() -> (
    gathers.apify_tiktok_accounts_posts.schemas.ApifyTikTokAccountsPostsGatherResponse
):
    """Example for ApifyTiktokAccountsGatherResponse schema."""
    return gathers.apify_tiktok_accounts_posts.schemas.ApifyTikTokAccountsPostsGatherResponse(
        name="Example",
        account_username_list=["@unitednations", "@bbcnews"],
        limit_posts_per_account=3,
        id=3,
        platform=gathers.schemas.Platform.tiktok,
        data_type=gathers.schemas.DataType.posts,
        source=gathers.schemas.Source.apify,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        project_id=1,
        deleted_at=None,
        latest_job_run=None,
        child_type=gathers.schemas.ChildTypeName.apify_tiktok_accounts_posts,
    )
