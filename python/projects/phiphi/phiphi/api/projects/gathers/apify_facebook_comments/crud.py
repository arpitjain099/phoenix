"""Apify facebook comments gather crud."""
# import sqlalchemy.orm
# from phiphi.api.projects.gathers import child_crud
# from phiphi.api.projects.gathers.apify_facebook_comments import models, schemas


# def create_apify_facebook_comment_gather(
#     session: sqlalchemy.orm.Session,
#     project_id: int,
#     request_schema: schemas.ApifyFacebookCommentGatherCreate,
# ) -> schemas.ApifyFacebookCommentGatherResponse:
#     """Create a new apify facebook post gather."""
#     return child_crud.create_child_gather(
#         reseponseModel=schemas.ApifyFacebookCommentGatherResponse,
#         session=session,
#         project_id=project_id,
#         request_schema=request_schema,
#         child_model=models.ApifyFacebookCommentGather,
#     )
