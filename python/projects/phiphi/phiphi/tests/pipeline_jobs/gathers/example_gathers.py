"""Example gathers (reponses/rows/specs)."""
import datetime

from phiphi.api.projects import gathers


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
