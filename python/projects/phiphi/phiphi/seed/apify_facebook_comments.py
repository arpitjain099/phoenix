"""Seed the apify facebook COMMENT gathers."""
from sqlalchemy.orm import Session

from phiphi.api.projects.gathers import child_crud as gather_child_crud
from phiphi.api.projects.gathers.apify_facebook_comments import models, schemas

CHILD_TYPE = "apify_facebook_comments"

TEST_APIFY_FACEBOOK_COMMENT_GATHER_CREATE = schemas.ApifyFacebookCommentGatherCreate(
    description="Phoenix Apify Facebook COMMENT Gather",
    post_url_list=["https://phoenix.com", "https://buildup.org"],
    limit_comments_per_post=1000,
    sort_comments_by=schemas.SortComment.facebook_default,
    include_comment_replies=False,
)

TEST_APIFY_FACEBOOK_COMMENT_GATHER_CREATE_2 = schemas.ApifyFacebookCommentGatherCreate(
    description="Phoenix Apify Facebook COMMENT Gather 2",
    post_url_list=["https://phoenix.com", "https://buildup.org"],
    limit_comments_per_post=1000,
    sort_comments_by=schemas.SortComment.most_relevant,
    include_comment_replies=True,
)

TEST_APIFY_FACEBOOK_COMMENT_GATHER_CREATE_3 = schemas.ApifyFacebookCommentGatherCreate(
    description="Phoenix Apify Facebook COMMENT Gather 3",
    post_url_list=["https://phoenix.com"],
    limit_comments_per_post=1000,
    sort_comments_by=schemas.SortComment.newest_first,
    include_comment_replies=False,
)


def seed_test_apify_facebook_comment_gathers(session: Session) -> None:
    """Seed the gathers."""
    apify_facebook_gathers = [
        TEST_APIFY_FACEBOOK_COMMENT_GATHER_CREATE,
        TEST_APIFY_FACEBOOK_COMMENT_GATHER_CREATE_2,
    ]

    for apify_facebook_gather in apify_facebook_gathers:
        gather_child_crud.create_child_gather(
            session=session,
            project_id=2,
            request_schema=apify_facebook_gather,
            child_model=models.ApifyFacebookCommentGather,
            response_schema=schemas.ApifyFacebookCommentGatherResponse,
            child_type=CHILD_TYPE,
        )

    gather_child_crud.create_child_gather(
        session=session,
        project_id=1,
        request_schema=TEST_APIFY_FACEBOOK_COMMENT_GATHER_CREATE_3,
        child_model=models.ApifyFacebookCommentGather,
        response_schema=schemas.ApifyFacebookCommentGatherResponse,
        child_type=CHILD_TYPE,
    )
