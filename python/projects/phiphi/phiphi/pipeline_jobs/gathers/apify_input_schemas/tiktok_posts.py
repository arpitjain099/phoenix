"""Pydantic input schema for the Apify Tiktok posts scraper."""
import enum
from typing import List, Optional

import pydantic

from phiphi.pipeline_jobs.gathers.apify_input_schemas.types import UrlStr


class TiktokSearchSection(str, enum.Enum):
    """Enum for search section sorting options."""

    VIDEO = "video"
    USER = "user"


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
