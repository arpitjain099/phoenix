"""Seed the apify facebook post gathers."""
from sqlalchemy.orm import Session

from phiphi.api.projects.gathers import child_crud as gather_child_crud
from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.api.projects.gathers.apify_facebook_posts import models, schemas

TEST_APIFY_FACEBOOK_POST_GATHER_CREATE = schemas.ApifyFacebookPostGatherCreate(
    description="Phoenix Apify Facebook Post Gather",
    author_url_list=["https://phoenix.com", "https://buildup.org"],
    limit_posts_per_account=1000,
    only_posts_older_than="2024-04-25",
    only_posts_newer_than="2024-05-02",
    source=gather_schemas.Source.apify,
    platform=gather_schemas.Platform.facebook,
    data_type=gather_schemas.DataType.posts,
)

TEST_APIFY_FACEBOOK_POST_GATHER_CREATE_2 = schemas.ApifyFacebookPostGatherCreate(
    description="Phoenix Apify Facebook Post Gather 2",
    author_url_list=["https://phoenix.com", "https://buildup.org"],
    limit_posts_per_account=1000,
    only_posts_older_than="2024-03-12",
    only_posts_newer_than="2024-05-01",
    source=gather_schemas.Source.apify,
    platform=gather_schemas.Platform.facebook,
    data_type=gather_schemas.DataType.posts,
)

TEST_APIFY_FACEBOOK_POST_GATHER_CREATE_3 = schemas.ApifyFacebookPostGatherCreate(
    description="Phoenix Apify Facebook Post Gather 3",
    author_url_list=["https://phoenix.com"],
    limit_posts_per_account=1000,
    only_posts_older_than="2024-02-25",
    only_posts_newer_than="2024-05-03",
    source=gather_schemas.Source.apify,
    platform=gather_schemas.Platform.facebook,
    data_type=gather_schemas.DataType.posts,
)


def seed_test_apify_facebook_post_gathers(session: Session) -> None:
    """Seed the gathers."""
    apify_facebook_gathers = [
        TEST_APIFY_FACEBOOK_POST_GATHER_CREATE,
        TEST_APIFY_FACEBOOK_POST_GATHER_CREATE_2,
    ]

    for apify_facebook_gather in apify_facebook_gathers:
        gather_child_crud.create_child_gather(  # type: ignore[type-var]
            session=session,
            project_id=1,
            request_schema=apify_facebook_gather,
            child_model=models.ApifyFacebookPostGather,
            response_schema=schemas.ApifyFacebookPostGatherResponse,
        )

    gather_child_crud.create_child_gather(  # type: ignore[type-var]
        session=session,
        project_id=2,
        request_schema=TEST_APIFY_FACEBOOK_POST_GATHER_CREATE_3,
        child_model=models.ApifyFacebookPostGather,
        response_schema=schemas.ApifyFacebookPostGatherResponse,
    )
