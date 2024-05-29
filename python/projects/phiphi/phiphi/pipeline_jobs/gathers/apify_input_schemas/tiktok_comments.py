"""Pydantic input schema for the Apify TikTok comments scraper."""
from typing import List

import pydantic

from phiphi.pipeline_jobs.gathers.apify_input_schemas.types import UrlStr


class ApifyTiktokCommentsInput(pydantic.BaseModel):
    """Input schema for the TikTok Comments Scraper.

    Facilitates the extraction of comments from specific TikTok videos by providing URLs.

    Ref Apify actor docs: https://apify.com/clockworks/tiktok-comments-scraper/input-schema
    """

    post_urls: List[UrlStr] = pydantic.Field(
        serialization_alias="postURLs",
        description="List of URLs for TikTok videos from which to scrape comments.",
    )
    comments_per_post: int = pydantic.Field(
        default=25,
        serialization_alias="commentsPerPost",
        description=(
            "Maximum number of comments to scrape from each video; defaults to 100. "
            "Over 500 can be slow."
        ),
    )
    max_replies_per_comment: int = pydantic.Field(
        default=0,
        serialization_alias="maxRepliesPerComment",
        description="Docs say 'Slow'. Maximum number of replies to scrape from each comment; "
        "defaults to 0. NOTE: it is currently not guaranteed that the scraper will manage to "
        "scrape ALL the desired replies. By default no replies are scraped.",
    )

    class Config:
        """Pydantic configuration."""

        extra = pydantic.Extra.forbid
