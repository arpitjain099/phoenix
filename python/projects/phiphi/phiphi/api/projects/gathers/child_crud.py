"""Generic gather crud."""
from typing import Type, TypeVar

import sqlalchemy.orm

from phiphi.api.projects import crud as project_crud
from phiphi.api.projects.gathers import child_types
from phiphi.api.projects.gathers import models as gather_model
from phiphi.api.projects.gathers import schemas as gather_schema
from phiphi.api.projects.gathers.apify_facebook_comments import (
    models as facebook_comment_models,  # noqa: F401
)
from phiphi.api.projects.gathers.apify_facebook_posts import (
    models as facebook_post_models,  # noqa: F401
)

# Although these are the same as child_route types we need to redefine them here
# otherwise we get strange errors
response_schema_type = TypeVar("response_schema_type", bound=gather_schema.GatherResponse)
create_schema_type = TypeVar("create_schema_type", bound=gather_schema.GatherCreate)
child_model_type = TypeVar("child_model_type", bound=gather_model.Gather)


def create_child_gather(
    response_schema: Type[response_schema_type],
    session: sqlalchemy.orm.Session,
    project_id: int,
    request_schema: create_schema_type,
    child_model: Type[child_model_type],
    child_type: gather_schema.ChildType,
) -> response_schema_type:
    """Create child gather.

    A generalised function to create a child gather. This function is used to create
    child gathers for different platforms and data types.

    Args:
        response_schema (Type[response_schema_type]): Response schema
        session (sqlalchemy.orm.Session): Database session
        project_id (int): Project id
        request_schema (create_schema_type): Request schema
        child_model (Type[child_model_type]): Child model
        child_type (str): Child type

    Returns:
        response_schema_type: Response schema
    """
    project_crud.get_db_project_with_guard(session, project_id)

    split_child_type = child_type.split("_")
    source = split_child_type[0]
    platform = split_child_type[1]
    data_type = split_child_type[2]

    db_apify_facebook_post_gather = child_model(
        **request_schema.dict(),
        platform=platform,
        data_type=data_type,
        source=source,
        project_id=project_id,
        child_type=child_type,
    )
    session.add(db_apify_facebook_post_gather)
    session.commit()
    session.refresh(db_apify_facebook_post_gather)
    return response_schema.model_validate(db_apify_facebook_post_gather)


def get_child_gather(
    session: sqlalchemy.orm.Session,
    project_id: int,
    gather_id: int,
) -> gather_schema.GatherResponse | None:
    """Get a child gather.

    A generalised function to get a child gather. This function is used to get
    child gathers for different platforms and data types.
    """
    db_gather = (
        session.query(gather_model.Gather)
        .filter(
            gather_model.Gather.deleted_at.is_(None),
            gather_model.Gather.project_id == project_id,
            gather_model.Gather.id == gather_id,
        )
        .first()
    )
    if db_gather is None:
        return None

    child_type = gather_schema.ChildType(db_gather.child_type)
    child_reponse_type: child_types.ALL_TYPE = child_types.get_response_type(child_type)
    return child_reponse_type.model_validate(db_gather)
