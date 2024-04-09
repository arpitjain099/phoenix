"""Seed the gathers."""
import datetime

from sqlalchemy.orm import Session

from phiphi.api.gathers import crud, schemas

TEST_APIFY_GATHER_CREATE = schemas.ApifyGatherCreate(
    description="Phoenix Apify Gather",
    instance_id=1,
    input_type=schemas.ApifyGatherInputType.author_url_list,
    input_data="lorem ipsum",
    platform=schemas.Platform.facebook,
    data_type=schemas.DataType.messages,
    start_date=datetime.datetime.now(),
    end_date=datetime.datetime.now(),
    limit_messages=1000,
    limit_replies=100,
    nested_replies=False,
)

TEST_APIFY_GATHER_CREATE_2 = schemas.ApifyGatherCreate(
    description="Phoenix Apify Gather 2",
    instance_id=1,
    input_type=schemas.ApifyGatherInputType.author_url_list,
    input_data="lorem ipsum",
    platform=schemas.Platform.facebook,
    data_type=schemas.DataType.messages,
    start_date=datetime.datetime.now(),
    end_date=datetime.datetime.now(),
    limit_messages=1000,
    limit_replies=100,
    nested_replies=False,
)


def seed_test_apify_gathers(session: Session) -> None:
    """Seed the gathers."""
    apify_gathers = [TEST_APIFY_GATHER_CREATE, TEST_APIFY_GATHER_CREATE_2]

    for apify_gather in apify_gathers:
        crud.create_apify_gather(session=session, gather_data=apify_gather)
