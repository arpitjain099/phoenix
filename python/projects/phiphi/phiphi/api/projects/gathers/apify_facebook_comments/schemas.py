"""Schemas for apify facebook comments gathers."""
import enum
from typing import Any, Dict, List, Optional

import pydantic

from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.pydantic_types import UrlStr


class FacebookCommentSortOption(str, enum.Enum):
    """Enum for the sorting options for Facebook comments."""

    facebook_default = "facebook_default"
    most_relevant = "most_relevant"
    newest_first = "newest_first"
    non_filtered = "non_filtered"


apify_facebook_comment_sort_option_mapping = {
    FacebookCommentSortOption.facebook_default: "RANKED_UNFILTERED",
    FacebookCommentSortOption.most_relevant: "RANKED_THREADED",
    FacebookCommentSortOption.newest_first: "RECENT_ACTIVITY",
    FacebookCommentSortOption.non_filtered: "RANKED_UNFILTERED",
}


class ApifyFacebookCommentGatherBase(gather_schemas.GatherBase):
    """Input schema for the Apify Facebook comments scraper.

    Ref to relevant Apify actor docs: https://apify.com/apify/facebook-comments-scraper/input-schema
    """

    limit_comments_per_post: int = pydantic.Field(
        serialization_alias="resultsLimit",
        description="Limit results per post; defaults to 50 if not set",
    )
    post_url_list: List[UrlStr] = pydantic.Field(
        ...,
        serialization_alias="startUrls",
        description="List of Facebook post URLs to scrape comments from",
    )
    sort_comments_by: Optional[FacebookCommentSortOption] = pydantic.Field(
        default=None,
        serialization_alias="viewOption",
        description="Sorting option for comments, default is 'RANKED_UNFILTERED'",
    )
    include_comment_replies: bool = pydantic.Field(
        default=False,
        serialization_alias="includeNestedComments",
        description=(
            "If True, includes up to 3 levels of nested comments/replies. "
            "WARNING: this breaks results_limit and will likely return more comments "
            "and incur more cost than expected."
        ),
    )


class ApifyFacebookCommentGatherResponse(
    gather_schemas.GatherResponse, ApifyFacebookCommentGatherBase
):
    """Apify Facebook Comments Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)

    def serialize_to_apify_input(self) -> Dict[str, Any]:
        """Serialize the instance to a dictionary suitable for Apify API."""
        apify_dict = super().serialize_to_apify_input()
        if "startUrls" in apify_dict:
            apify_dict["startUrls"] = self.serialize_comment_urls(apify_dict["startUrls"])
        if "viewOption" in apify_dict:
            apify_dict["viewOption"] = self.serialize_sort_comments_by(apify_dict["viewOption"])
        return apify_dict

    @staticmethod
    def serialize_comment_urls(urls: List[str]) -> List[Dict[str, str]]:
        """Convert a list of plain URLs to the list of dicts required for Apify."""
        return [{"url": str(url)} for url in urls]

    @staticmethod
    def serialize_sort_comments_by(value: Optional[FacebookCommentSortOption]) -> Optional[str]:
        """Serialize sort_comments_by."""
        return apify_facebook_comment_sort_option_mapping[value] if value else None


class ApifyFacebookCommentGatherCreate(
    ApifyFacebookCommentGatherBase, gather_schemas.GatherCreate
):
    """Apify Facebook Comments  Gather create schema.

    Properties to receive via API on creation.
    """


class ApifyFacebookCommentGatherUpdate(gather_schemas.GatherUpdate):
    """Apify Facebook Comments  Gather update schema."""
