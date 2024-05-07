"""Routes for gathers."""
from typing import Callable

import fastapi
from phiphi.api import deps
from phiphi.api.projects.gathers import child_crud
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

list_of_child_gather_routes = {
    "apify_facebook_comment": (
        facebook_comment_schema.ApifyFacebookCommentGatherCreate,
        facebook_comment_schema.ApifyFacebookCommentGatherResponse,
        facebook_comment_model.ApifyFacebookCommentGather,
    ),
    "apify_facebook_post": (
        facebook_post_schema.ApifyFacebookPostGatherCreate,
        facebook_post_schema.ApifyFacebookPostGatherResponse,
        facebook_post_model.ApifyFacebookPostGather,
    ),
    # Add more routes as needed
}


def make_create_child_gather_route(request_schema, response_schema, child_model) -> Callable:  # type: ignore[no-untyped-def]
    """Returns a route function that creates a child gather using specific models."""

    def create_child_gather(  # type: ignore[no-any-unimported]
        project_id: int,
        request: request_schema,
        session: deps.SessionDep,
    ) -> response_schema:
        """Generic route for child gather creation."""
        return child_crud.create_child_gather(
            response_schema=response_schema,
            request_schema=request,
            child_model=child_model,
            project_id=project_id,
            session=session,
        )

    return create_child_gather


# Register all routes
for key, (request_schema, response_schema, child_model) in list_of_child_gather_routes.items():
    router.post(
        f"/projects/{{project_id}}/gathers/{key}",
        response_model=response_schema,  # The FastAPI route response model
    )(make_create_child_gather_route(request_schema, response_schema, child_model))
