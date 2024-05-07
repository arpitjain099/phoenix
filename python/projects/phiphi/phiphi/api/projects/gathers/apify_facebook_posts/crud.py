"""Apify facebook post gather crud."""
# import sqlalchemy.orm
# from phiphi.api.projects.gathers import child_crud
# from phiphi.api.projects.gathers.apify_facebook_posts import models, schemas


# def create_apify_facebook_post_gather(
#     session: sqlalchemy.orm.Session,
#     project_id: int,
#     request_schema: schemas.ApifyFacebookPostGatherCreate,
# ) -> schemas.ApifyFacebookPostGatherResponse:
#     """Create a new apify facebook post gather."""
#     return child_crud.create_child_gather(
#         reseponseModel=schemas.ApifyFacebookPostGatherResponse,
#         session=session,
#         project_id=project_id,
#         request_schema=request_schema,
#         child_model=models.ApifyFacebookPostGather,
#     )
