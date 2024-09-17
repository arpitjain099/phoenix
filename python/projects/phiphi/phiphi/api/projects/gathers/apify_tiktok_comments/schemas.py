"""Schemas for Apify TikTok comments.

After testing we decided to use `apidojo` instead of `clockworks` for scraping TikTok comments.
This is mainly due to the price difference.

For reference see the Apify actor docs:
https://apify.com/apidojo/tiktok-comments-scraper/input-schema
"""
from typing import Optional

import pydantic

from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.pydantic_types import UrlStr


class ApifyTikTokCommentsGatherBase(gather_schemas.GatherBase):
    """Input schema for the Apify TikTok Scraper for comments."""

    post_url_list: list[UrlStr] = pydantic.Field(
        serialization_alias="startUrls",
        description="List of TikTok post (video) URLs to scrape comments from",
    )
    limit_comments_per_post: int = pydantic.Field(
        serialization_alias="maxItems",
        description="Limit comments (including replies) per post (video)",
    )
    include_comment_replies: bool = pydantic.Field(
        default=False,
        serialization_alias="includeReplies",
        description="If True, includes replies to comments. Default is False.",
    )


class ApifyTikTokCommentsGatherResponse(
    gather_schemas.GatherResponse, ApifyTikTokCommentsGatherBase
):
    """Apify TikTok searches posts gather schema."""

    pass


class ApifyTikTokCommentsGatherCreate(ApifyTikTokCommentsGatherBase, gather_schemas.GatherCreate):
    """Apify TikTok Comments Gather create schema.

    Properties to receive via API on creation.
    """


class ApifyTikTokCommentsGatherUpdate(gather_schemas.GatherUpdate):
    """Apify TikTok Comments Gather update schema.

    Only properties that are set will be updated.
    """

    limit_comments_per_post: Optional[int] = pydantic.Field(
        default=None,
        description="Limit comments (including replies) per post (video)",
    )
    post_url_list: Optional[list[UrlStr]] = pydantic.Field(
        default=None,
        description="List of TikTok post (video) URLs to scrape comments from",
    )
    include_comment_replies: Optional[bool] = pydantic.Field(
        default=None,
        description="If True, includes replies to comments.",
    )
