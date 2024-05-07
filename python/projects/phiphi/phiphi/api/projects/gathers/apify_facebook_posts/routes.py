"""Routes for apify facebook post gather."""
# import fastapi
# from phiphi.api import deps
# from phiphi.api.projects.gathers.apify_facebook_posts import crud, schemas

# router = fastapi.APIRouter()


# @router.post(
#     "/projects/{project_id}/gathers/apify_facebook_posts",
#     response_model=schemas.ApifyFacebookPostGatherResponse,
# )
# def create_apify_facebook_post_gather(
#     gather: schemas.ApifyFacebookPostGatherCreate,
#     project_id: int,
#     session: deps.SessionDep,
# ) -> schemas.ApifyFacebookPostGatherResponse:
#     """Create a new apify facebook post gather."""
#     return crud.create_apify_facebook_post_gather(session, project_id, gather)
