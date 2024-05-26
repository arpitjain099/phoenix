"""Pydantic schemas for the Apify scrapers.

This modules contains a Pydantic schema for each Apify scraper, which:
    - Defines the data structure that we want to use in our system for that scraper.
    - Converts that data structure to the correct structure for the Apify API.
"""
import enum
from typing import Annotated, Dict, List, Optional, Union

import pydantic

http_url_adapter = pydantic.TypeAdapter(pydantic.HttpUrl)

UrlStr = Annotated[
    str, pydantic.BeforeValidator(lambda value: str(http_url_adapter.validate_python(value)))
]


class ApifyFacebookPostsInput(pydantic.BaseModel):
    """Input schema for the Apify Facebook posts scraper.

    Ref to relevant Apify actor docs: https://apify.com/apify/facebook-posts-scraper/input-schema
    """

    results_per_url_limit: int = pydantic.Field(
        25, serialization_alias="resultsLimit", description="Limit results per account"
    )
    account_urls: List[UrlStr] = pydantic.Field(
        serialization_alias="startUrls",
        description="List of Facebook page/profile URLs to scrape from",
    )
    only_posts_older_than: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="onlyPostsOlderThan",
        description="Fetch posts only older than this date (YYYY-MM-DD)",
    )
    only_posts_newer_than: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="onlyPostsNewerThan",
        description="Fetch posts only newer than this date (YYYY-MM-DD)",
    )

    class Config:
        """Pydantic configuration."""

        extra = pydantic.Extra.forbid

    @pydantic.field_serializer("account_urls")
    def serialize_account_urls(self, urls: List[pydantic.HttpUrl]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]


class FacebookCommentSortOption(str, enum.Enum):
    """Enum for the sorting options for Facebook comments."""

    RANKED_THREADED = "RANKED_THREADED"
    RECENT_ACTIVITY = "RECENT_ACTIVITY"
    RANKED_UNFILTERED = "RANKED_UNFILTERED"


class ApifyFacebookCommentsInput(pydantic.BaseModel):
    """Input schema for the Apify Facebook comments scraper.

    Ref to relevant Apify actor docs: https://apify.com/apify/facebook-comments-scraper/input-schema
    """

    post_urls: List[UrlStr] = pydantic.Field(
        ...,
        serialization_alias="startUrls",
        description="List of Facebook post URLs to scrape comments from",
    )
    results_limit: int = pydantic.Field(
        25,
        serialization_alias="resultsLimit",
        description="Limit results per post; defaults to 50 if not set",
    )
    include_nested_comments: bool = pydantic.Field(
        default=False,
        serialization_alias="includeNestedComments",
        description=(
            "If True, includes up to 3 levels of nested comments/replies. "
            "WARNING: this breaks results_limit and will likely return more comments "
            "and incur more cost than expected."
        ),
    )
    comment_sort_option: Optional[FacebookCommentSortOption] = pydantic.Field(
        default=None,
        serialization_alias="viewOption",
        description="Sorting option for comments, default is 'RANKED_UNFILTERED'",
    )

    class Config:
        """Pydantic configuration."""

        extra = pydantic.Extra.forbid

    @pydantic.field_serializer("post_urls")
    def serialize_account_urls(self, urls: List[pydantic.HttpUrl]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]


class TiktokSearchSection(str, enum.Enum):
    """Enum for search section sorting options."""

    VIDEO = "/video"
    USER = "/user"


class ApifyTiktokPostsInput(pydantic.BaseModel):
    """Input schema for the TikTok Scraper.

    Enables scraping data from TikTok based on various inputs like direct URLs, hashtags, or search
    queries.

    Ref to relevant Apify actor docs: https://apify.com/clockworks/tiktok-scraper/input-schema
    """

    results_per_page: int = pydantic.Field(
        25,
        serialization_alias="resultsPerPage",
        description=(
            "Number of TikTok videos to scrape per hashtag, profile, or search query. "
            "This field is applicable to hashtags, profiles, and search."
        ),
    )
    hashtags: Optional[List[str]] = pydantic.Field(
        default=None,
        serialization_alias="hashtags",
        description="List of hashtags to scrape TikTok videos for.",
    )
    profiles: Optional[List[str]] = pydantic.Field(
        default=None,
        serialization_alias="profiles",
        description="List of TikTok usernames to scrape.",
    )
    search_queries: Optional[List[str]] = pydantic.Field(
        default=None,
        serialization_alias="searchQueries",
        description="Search queries to apply across videos and profiles.",
    )
    search_section: Optional[TiktokSearchSection] = pydantic.Field(
        default=None,
        serialization_alias="searchSection",
        description="Specifies where to apply the search query: to videos or profiles.",
    )
    post_urls: Optional[List[UrlStr]] = pydantic.Field(
        default=None,
        serialization_alias="postURLs",
        description="Direct URLs of TikTok videos to scrape.",
    )
    oldest_post_date: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="oldestPostDate",
        description="Scrape profile videos uploaded after or on this date.",
    )
    scrape_last_n_days: Optional[int] = pydantic.Field(
        default=None,
        serialization_alias="scrapeLastNDays",
        description="Scrape profile videos from the last specified number of days.",
    )
    max_profiles_per_query: Optional[int] = pydantic.Field(
        default=None,
        serialization_alias="maxProfilesPerQuery",
        description=(
            "Only applies to profile searches. In this case ignore the 100 number of videos "
            "section and choose the number of profiles you want to scrape here."
        ),
    )
    should_download_videos: bool = pydantic.Field(
        default=False,
        serialization_alias="shouldDownloadVideos",
        description="Set to true to download TikTok videos.",
    )
    should_download_covers: bool = pydantic.Field(
        default=False,
        serialization_alias="shouldDownloadCovers",
        description="Set to true to download TikTok video covers (thumbnails).",
    )
    should_download_subtitles: bool = pydantic.Field(
        default=False,
        serialization_alias="shouldDownloadSubtitles",
        description="Set to true to download subtitles for TikTok videos.",
    )
    should_download_slideshow_images: bool = pydantic.Field(
        default=False,
        serialization_alias="shouldDownloadSlideshowImages",
        description="Set to true to download TikTok slideshow images.",
    )
    video_kv_store_id_or_name: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="videoKvStoreIdOrName",
        description="Name or ID of the Key Value Store for storing downloaded media.",
    )
    proxy_country_code: Optional[str] = pydantic.Field(
        default=None,
        serialization_alias="proxyCountryCode",
        description="2 letter proxy country code to use if scraping location-specific content.",
    )

    class Config:
        """Pydantic configuration."""

        extra = pydantic.Extra.forbid


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


ApifyInputType = Union[
    ApifyFacebookPostsInput,
    ApifyFacebookCommentsInput,
    ApifyTiktokPostsInput,
    ApifyTiktokCommentsInput,
]
