"""Seed the gathers."""
import datetime

from sqlalchemy.orm import Session

from phiphi.api.projects.gathers import crud, schemas

TEST_APIFY_GATHER_CREATE = schemas.ApifyGatherCreate(
    description="Phoenix Apify Gather",
    input=schemas.InputAuthorList(
        type=schemas.ApifyGatherInputType.author_url_list, data=["author_1", "author_2"]
    ),
    platform=schemas.Platform.facebook,
    data_type=schemas.DataType.posts,
    start_date=datetime.datetime.now() - datetime.timedelta(days=7),
    end_date=datetime.datetime.now(),
    limit_messages=1000,
    limit_replies=100,
    nested_replies=False,
)

TEST_APIFY_GATHER_CREATE_2 = schemas.ApifyGatherCreate(
    description="Phoenix Apify Gather 2",
    input=schemas.InputAuthorList(
        type=schemas.ApifyGatherInputType.author_url_list, data=["author_1"]
    ),
    platform=schemas.Platform.facebook,
    data_type=schemas.DataType.posts,
    start_date=datetime.datetime.now() - datetime.timedelta(days=7),
    end_date=datetime.datetime.now() + datetime.timedelta(days=1),
    limit_messages=1000,
    limit_replies=100,
    nested_replies=False,
)

TEST_APIFY_GATHER_CREATE_3 = schemas.ApifyGatherCreate(
    description="Phoenix Apify Gather 3",
    input=schemas.InputAuthorList(
        type=schemas.ApifyGatherInputType.author_url_list, data=["author_3", "author_4"]
    ),
    platform=schemas.Platform.facebook,
    data_type=schemas.DataType.posts,
    start_date=datetime.datetime.now() - datetime.timedelta(days=5),
    end_date=datetime.datetime.now() + datetime.timedelta(days=2),
    limit_messages=150,
    limit_replies=10,
    nested_replies=True,
)


def seed_test_apify_gathers(session: Session) -> None:
    """Seed the gathers."""
    apify_gathers = [TEST_APIFY_GATHER_CREATE, TEST_APIFY_GATHER_CREATE_2]

    for apify_gather in apify_gathers:
        crud.create_apify_gather(session=session, project_id=1, gather_data=apify_gather)

    crud.create_apify_gather(session=session, project_id=2, gather_data=TEST_APIFY_GATHER_CREATE_3)
