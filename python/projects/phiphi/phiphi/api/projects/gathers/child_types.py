"""Child types."""
from typing import Type, Union

from phiphi.api.projects.gathers import schemas as gather_schemas
from phiphi.api.projects.gathers.apify_facebook_comments import (
    schemas as facebook_comment_schema,
)
from phiphi.api.projects.gathers.apify_facebook_posts import (
    schemas as facebook_post_schema,
)

ALL = Union[
    facebook_comment_schema.ApifyFacebookCommentGatherResponse,
    facebook_post_schema.ApifyFacebookPostGatherResponse,
]

ALL_TYPE = Type[ALL]

CHILD_TYPES_MAP: dict[gather_schemas.ChildTypeName, ALL_TYPE] = {
    gather_schemas.ChildTypeName.apify_facebook_comments: (
        facebook_comment_schema.ApifyFacebookCommentGatherResponse
    ),
    gather_schemas.ChildTypeName.apify_facebook_posts: (
        facebook_post_schema.ApifyFacebookPostGatherResponse
    ),
}


def get_response_type(gather_child_type: gather_schemas.ChildTypeName) -> ALL_TYPE:
    """Get response type.

    Args:
        gather_child_type (gather_schemas.ChildTypeName): Gather child type

    Returns:
        response_schema_type: Response schema type
    """
    if gather_child_type not in CHILD_TYPES_MAP:
        raise ValueError(
            f"Gather child_type: {gather_child_type} has not been added to CHILD_TYPES_MAP."
            " This should be done."
        )
    return CHILD_TYPES_MAP[gather_child_type]
