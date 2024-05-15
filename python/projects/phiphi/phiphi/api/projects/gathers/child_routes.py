"""Routes for child gathers.

This module contains generalised functionality for creating child gathers. This is used to create
child gathers for different platforms and data types, so we don't repeat the same code for each
child gather type.

To add a new child gather route, add a new entry to `list_of_child_gather_routes` with the request
schema, response schema, and child model for the new child gather route. Then add a new call to
`router.post` with the route path and response model for the new child gather route.

Please note that there are a number of complexity issues with mypy and making a generic route. As
such there are a number of `# type: ignore[valid-type]` comments in this file. This is because the
typing was getting complex and we decided to ignore the typing errors.
"""
from typing import Callable, Type, TypeVar

import fastapi
from phiphi.api import deps
from phiphi.api.projects.gathers import child_crud
from phiphi.api.projects.gathers import models as gather_model
from phiphi.api.projects.gathers import schemas as gather_schema
from phiphi.api.projects.gathers.apify_facebook_comments import (
    models as facebook_comment_model,
)
from phiphi.api.projects.gathers.apify_facebook_comments import (
    schemas as facebook_comment_schema,
)
from phiphi.api.projects.gathers.apify_facebook_posts import (
    models as facebook_post_model,
)
from phiphi.api.projects.gathers.apify_facebook_posts import (
    schemas as facebook_post_schema,
)

router = fastapi.APIRouter()

# Although these are the same as child_crud types we need to redefine them here
# otherwise we get strange errors
response_schema_type = TypeVar("response_schema_type", bound=gather_schema.GatherResponse)
create_schema_type = TypeVar("create_schema_type", bound=gather_schema.GatherCreate)
child_model_type = TypeVar("child_model_type", bound=gather_model.Gather)

list_of_child_gather_routes: dict[
    str,
    tuple[
        Type[gather_schema.GatherCreate],
        Type[gather_schema.GatherResponse],
        Type[gather_model.Gather],
    ],
] = {
    "apify_facebook_comments": (
        facebook_comment_schema.ApifyFacebookCommentGatherCreate,
        facebook_comment_schema.ApifyFacebookCommentGatherResponse,
        facebook_comment_model.ApifyFacebookCommentGather,
    ),
    "apify_facebook_posts": (
        facebook_post_schema.ApifyFacebookPostGatherCreate,
        facebook_post_schema.ApifyFacebookPostGatherResponse,
        facebook_post_model.ApifyFacebookPostGather,
    ),
    # Add more routes as needed
}


def make_create_child_gather_route(
    request_schema: Type[create_schema_type],
    response_schema: Type[response_schema_type],
    child_model: Type[child_model_type],
    child_type: str,
) -> Callable[[int, create_schema_type, deps.SessionDep], response_schema_type]:
    """Returns a route function that creates a child gather using specific models.

    This function is used so that the given types for the route can be passed in as arguments to
    the function. If we don't use this wrapper function we the types of the last item in
    list_of_child_gather_routes will be used for all routes.
    """

    # We decided to do type ignore here, because the typing was getting complex
    def create_child_gather(
        project_id: int,
        request: request_schema,  # type: ignore[valid-type]
        session: deps.SessionDep,
    ) -> response_schema:  # type: ignore[valid-type]
        """Generic route for child gather creation."""
        return child_crud.create_child_gather(
            response_schema=response_schema,
            request_schema=request,
            child_model=child_model,
            project_id=project_id,
            session=session,
            child_type=child_type,
        )

    return create_child_gather


# Register all routes in list_of_child_gather_routes so we don't have to rewrite the same code
for key, (request_schema, response_schema, child_model) in list_of_child_gather_routes.items():
    router.post(
        f"/projects/{{project_id}}/gathers/{key}",
        response_model=response_schema,
    )(make_create_child_gather_route(request_schema, response_schema, child_model, key))
