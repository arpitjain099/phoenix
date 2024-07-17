"""Child types."""
from typing import Any, Type, Union

from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.api.projects.gathers.apify_facebook_comments import (
    schemas as facebook_comment_schema,
)
from phiphi.api.projects.gathers.apify_facebook_posts import (
    schemas as facebook_post_schema,
)
from phiphi.api.projects.gathers.apify_tiktok_accounts_posts import (
    schemas as tiktok_accounts_posts_schema,
)
from phiphi.api.projects.gathers.apify_tiktok_hashtags_posts import (
    schemas as tiktok_hashtags_posts_schema,
)

##############################
# Child Types
#
# IMPORTANT:
# Add AllChildTypesUnion and CHILD_TYPES_MAP.
##############################
AllChildTypesUnion = Union[
    facebook_comment_schema.ApifyFacebookCommentsGatherResponse,
    facebook_post_schema.ApifyFacebookPostsGatherResponse,
    tiktok_hashtags_posts_schema.ApifyTikTokHashtagsPostsGatherResponse,
    tiktok_accounts_posts_schema.ApifyTikTokAccountsPostsGatherResponse,
]

CHILD_TYPES_MAP: dict[gather_schemas.ChildTypeName, Type[AllChildTypesUnion]] = {
    gather_schemas.ChildTypeName.apify_facebook_comments: (
        facebook_comment_schema.ApifyFacebookCommentsGatherResponse
    ),
    gather_schemas.ChildTypeName.apify_facebook_posts: (
        facebook_post_schema.ApifyFacebookPostsGatherResponse
    ),
    gather_schemas.ChildTypeName.apify_tiktok_hashtags_posts: (
        tiktok_hashtags_posts_schema.ApifyTikTokHashtagsPostsGatherResponse
    ),
    gather_schemas.ChildTypeName.apify_tiktok_accounts_posts: (
        tiktok_accounts_posts_schema.ApifyTikTokAccountsPostsGatherResponse
    ),
}

CHILD_TYPES_MAP_CREATE_DEFAULTS: dict[gather_schemas.ChildTypeName, dict[str, str]] = {
    gather_schemas.ChildTypeName.apify_facebook_posts: {
        "source": gather_schemas.Source.apify,
        "platform": gather_schemas.Platform.facebook,
        "data_type": gather_schemas.DataType.posts,
    },
    gather_schemas.ChildTypeName.apify_facebook_comments: {
        "source": gather_schemas.Source.apify,
        "platform": gather_schemas.Platform.facebook,
        "data_type": gather_schemas.DataType.comments,
    },
    gather_schemas.ChildTypeName.apify_tiktok_accounts_posts: {
        "source": gather_schemas.Source.apify,
        "platform": gather_schemas.Platform.tiktok,
        "data_type": gather_schemas.DataType.posts,
    },
}


def get_response_type(
    child_type_name: gather_schemas.ChildTypeName,
) -> Type[AllChildTypesUnion]:
    """Get response type.

    Args:
        child_type_name (gather_schemas.ChildTypeName): Gather child type

    Returns:
        response_schema_type: Response schema type for the child type.
    """
    if child_type_name not in CHILD_TYPES_MAP:
        raise ValueError(
            f"Gather child_type: {child_type_name} has not been added to CHILD_TYPES_MAP."
            " This should be done."
        )
    return CHILD_TYPES_MAP[child_type_name]


def get_create_defaults(
    child_type_name: gather_schemas.ChildTypeName,
) -> dict[str, Any]:
    """Get create defaults for a child gather.

    Args:
        child_type_name (gather_schemas.ChildTypeName): Gather child type

    Returns:
        dict[str, str]: Create defaults for the child type.
    """
    if child_type_name not in CHILD_TYPES_MAP_CREATE_DEFAULTS:
        raise ValueError(
            f"Gather child_type: {child_type_name} has not been added to "
            "CHILD_TYPES_MAP_CREATE_DEFAULTS. "
            "This should be done."
        )
    return CHILD_TYPES_MAP_CREATE_DEFAULTS[child_type_name]
