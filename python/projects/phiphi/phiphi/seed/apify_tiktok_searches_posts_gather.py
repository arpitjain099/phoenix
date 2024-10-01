"""Seed the apify tiktok searches post gathers."""
from sqlalchemy.orm import Session

from phiphi.api.projects.gathers import child_crud as gather_child_crud
from phiphi.api.projects.gathers import schemas as gathers_schemas
from phiphi.api.projects.gathers.apify_tiktok_searches_posts import models, schemas

TEST_APIFY_TIKTOK_SEARCHES_POSTS_GATHER_CREATE = schemas.ApifyTikTokSearchesPostsGatherCreate(
    name="Phoenix Apify TikTok Searches Posts Gather",
    search_list=["search1", "search2"],
    limit_posts_per_search=1000,
    proxy_country_to_gather_from="US",
)

TEST_APIFY_TIKTOK_SEARCHES_POSTS_GATHERS = []


def seed_test_apify_tiktok_searches_posts_gathers(session: Session) -> None:
    """Seed the gathers."""
    apify_tiktok_gathers = [
        TEST_APIFY_TIKTOK_SEARCHES_POSTS_GATHER_CREATE,
    ]

    for apify_tiktok_gather in apify_tiktok_gathers:
        tiktok_gather = gather_child_crud.create_child_gather(
            session=session,
            project_id=2,
            request_schema=apify_tiktok_gather,
            child_model=models.ApifyTikTokSearchesPostsGather,
            response_schema=schemas.ApifyTikTokSearchesPostsGatherResponse,
            child_type=gathers_schemas.ChildTypeName.apify_tiktok_searches_posts,
        )
        TEST_APIFY_TIKTOK_SEARCHES_POSTS_GATHERS.append(tiktok_gather)
