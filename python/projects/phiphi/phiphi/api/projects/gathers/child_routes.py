"""Routes for gathers."""
# from functools import partial
from typing import Type
from functools import partial

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
    "apify_facebook_post": (
        facebook_post_schema.ApifyFacebookPostGatherCreate,
        facebook_post_schema.ApifyFacebookPostGatherResponse,
        facebook_post_model.ApifyFacebookPostGather,
    ),
    "apify_facebook_comment": (
        facebook_comment_schema.ApifyFacebookCommentGatherCreate,
        facebook_comment_schema.ApifyFacebookCommentGatherResponse,
        facebook_comment_model.ApifyFacebookCommentGather,
    ),
    # Add more routes as needed
}

for key, (request_schema, response_schema, child_model) in list_of_child_gather_routes.items():
    crud_func = partial(child_crud.create_child_gather,  response_schema=response_schema,
            request_schema=request_schema,
            child_model=child_model)
    @router.post(
        f"/projects/{{project_id}}/gathers/{key}",
    )
    def create_child_gather(
        project_id: int,
        request_schema: request_schema,  # type: ignore[valid-type]
        deps: deps.SessionDep,
    ) -> response_schema:  # type: ignore[valid-type]
        """Generic routes for child gather."""
        return crud_func(
            project_id=project_id,
            session=deps,
        )
