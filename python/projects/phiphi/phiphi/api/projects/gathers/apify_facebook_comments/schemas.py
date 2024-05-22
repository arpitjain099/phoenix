"""Schemas for apify facebook comments gathers."""

from enum import Enum
from typing import Annotated

import pydantic

from phiphi.api.projects.gathers import schemas as gather_schemas


class SortComment(str, Enum):
    """SortComment enum."""

    facebook_default = "facebook_default"
    most_relevant = "most_relevant"
    newest_first = "newest_first"
    non_filtered = "non_filtered"


class ApifyFacebookCommentGatherBase(gather_schemas.GatherBase):
    """Apify Facebook Comments Gather config schema."""

    post_url_list: Annotated[
        list[str],
        pydantic.Field(description="The post url list, should be the full url including https"),
    ]

    limit_comments_per_post: Annotated[
        int,
        pydantic.Field(
            default=1000,
            description="Limit the number of comments per post",
        ),
    ]
    sort_comments_by: Annotated[
        SortComment,
        pydantic.Field(
            description="Sort the comments to gather. Can be used with `limit-comments_per_posts` "
            "to reduce costs and increase the relevance of the comments gathered.",
            default=SortComment.facebook_default,
        ),
    ]
    include_comment_replies: Annotated[
        bool,
        pydantic.Field(
            description="Includes the nested replies of comments.",
        ),
    ]


class ApifyFacebookCommentGatherResponse(
    gather_schemas.GatherResponse, ApifyFacebookCommentGatherBase
):
    """Apify Facebook Comments Gather schema.

    Properties to return to client.
    """

    model_config = pydantic.ConfigDict(from_attributes=True)


class ApifyFacebookCommentGatherCreate(
    ApifyFacebookCommentGatherBase, gather_schemas.GatherCreate
):
    """Apify Facebook Comments  Gather create schema.

    Properties to receive via API on creation.
    """


class ApifyFacebookCommentGatherUpdate(gather_schemas.GatherUpdate):
    """Apify Facebook Comments  Gather update schema."""
