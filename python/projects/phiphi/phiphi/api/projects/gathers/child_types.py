"""Child types."""
from typing import Type

from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.api.projects.gathers.apify_facebook_comments import (
    schemas as facebook_comment_schema,
)
from phiphi.api.projects.gathers.apify_facebook_posts import (
    schemas as facebook_post_schema,
)
from phiphi.api.projects.gathers.apify_tiktok_hashtags_posts import (
    schemas as tiktok_hashtags_posts_schema,
)

CHILD_TYPES_MAP: dict[gather_schemas.ChildTypeName, Type[gather_schemas.GatherResponse]] = {
    gather_schemas.ChildTypeName.apify_facebook_comments: (
        facebook_comment_schema.ApifyFacebookCommentGatherResponse
    ),
    gather_schemas.ChildTypeName.apify_facebook_posts: (
        facebook_post_schema.ApifyFacebookPostGatherResponse
    ),
    gather_schemas.ChildTypeName.apify_tiktok_hashtags_posts: (
        tiktok_hashtags_posts_schema.ApifyTikTokHashtagsPostsGatherResponse
    ),
}


def get_response_type(
    child_type_name: gather_schemas.ChildTypeName,
) -> Type[gather_schemas.GatherResponse]:
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
