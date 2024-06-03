"""Conftest for tests for the gather pipeline job."""
import pytest

from phiphi.api.projects import gathers
from phiphi.tests.pipeline_jobs.gathers import example_gathers


@pytest.fixture
def facebook_posts_gather_fixture() -> (
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse
):
    """Fixture for the Facebook posts gather example."""
    return example_gathers.facebook_posts_gather_example()


@pytest.fixture
def facebook_comments_gather_fixture() -> (
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse
):
    """Fixture for the Facebook comments gather example."""
    return example_gathers.facebook_comments_gather_example()
