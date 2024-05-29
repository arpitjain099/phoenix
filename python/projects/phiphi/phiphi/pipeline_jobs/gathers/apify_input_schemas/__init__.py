"""Pydantic schemas for the Apify scrapers.

This modules contains a Pydantic schema for each Apify scraper, which:
    - Defines the data structure that we want to use in our system for that scraper.
    - Converts that data structure to the correct structure for the Apify API.
"""
from typing import Union

from phiphi.pipeline_jobs.gathers.apify_input_schemas.facebook_comments import (
    ApifyFacebookCommentsInput,
)
from phiphi.pipeline_jobs.gathers.apify_input_schemas.facebook_posts import ApifyFacebookPostsInput
from phiphi.pipeline_jobs.gathers.apify_input_schemas.tiktok_comments import (
    ApifyTiktokCommentsInput,
)
from phiphi.pipeline_jobs.gathers.apify_input_schemas.tiktok_posts import ApifyTiktokPostsInput

ApifyInputType = Union[
    ApifyFacebookPostsInput,
    ApifyFacebookCommentsInput,
    ApifyTiktokPostsInput,
    ApifyTiktokCommentsInput,
]
