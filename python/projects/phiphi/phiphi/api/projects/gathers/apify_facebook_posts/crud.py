"""Apify facebook post gather crud."""
import sqlalchemy.orm
from phiphi.api.projects import crud as project_crud
from phiphi.api.projects.gathers.apify_facebook_posts import models, schemas


def create_apify_facebook_post_gather(
    session: sqlalchemy.orm.Session,
    project_id: int,
    gather_data: schemas.ApifyFacebookPostGatherCreate,
) -> schemas.ApifyFacebookPostGatherResponse:
    """Create a new apify facebook post gather."""
    project_crud.get_db_project_with_guard(session, project_id)

    source, platform, data_type = (gather_data.source, gather_data.platform, gather_data.data_type)

    if source and platform and data_type:
        child_type = f"{source.value}_{platform.value}_{data_type.value}"

    db_apify_facebook_post_gather = models.ApifyFacebookPostGather(
        **gather_data.dict(),
        project_id=project_id,
        child_type=child_type,
    )
    session.add(db_apify_facebook_post_gather)
    session.commit()
    session.refresh(db_apify_facebook_post_gather)
    return schemas.ApifyFacebookPostGatherResponse.model_validate(db_apify_facebook_post_gather)
