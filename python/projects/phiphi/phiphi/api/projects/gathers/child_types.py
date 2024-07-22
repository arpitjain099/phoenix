"""Child types."""
import dataclasses
from typing import Type, Union

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


@dataclasses.dataclass
class GatherCreationDefaults:
    """Gather creation defaults for a child gather."""

    platform: gather_schemas.Platform
    data_type: gather_schemas.DataType


CHILD_TYPES_MAP_CREATE_DEFAULTS: dict[gather_schemas.ChildTypeName, GatherCreationDefaults] = {
    gather_schemas.ChildTypeName.apify_facebook_comments: GatherCreationDefaults(
        platform=gather_schemas.Platform.facebook,
        data_type=gather_schemas.DataType.comments,
    ),
    gather_schemas.ChildTypeName.apify_facebook_posts: GatherCreationDefaults(
        platform=gather_schemas.Platform.facebook,
        data_type=gather_schemas.DataType.posts,
    ),
    gather_schemas.ChildTypeName.apify_tiktok_hashtags_posts: GatherCreationDefaults(
        platform=gather_schemas.Platform.tiktok,
        data_type=gather_schemas.DataType.posts,
    ),
    gather_schemas.ChildTypeName.apify_tiktok_accounts_posts: GatherCreationDefaults(
        platform=gather_schemas.Platform.tiktok,
        data_type=gather_schemas.DataType.posts,
    ),
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


def get_gather_creation_defaults(
    child_type_name: gather_schemas.ChildTypeName,
) -> GatherCreationDefaults:
    """Get gather creation defaults for a child gather.

    Args:
        child_type_name (gather_schemas.ChildTypeName): Gather child type

    Returns:
        GatherCreationDefaults: Create defaults for the child type.
    """
    if child_type_name not in CHILD_TYPES_MAP_CREATE_DEFAULTS:
        raise ValueError(
            f"Gather child_type: {child_type_name} has not been added to "
            "CHILD_TYPES_MAP_CREATE_DEFAULTS. "
            "This should be done."
        )
    return CHILD_TYPES_MAP_CREATE_DEFAULTS[child_type_name]
