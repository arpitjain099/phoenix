"""Generic gather crud."""
from typing import Type, TypeVar

import sqlalchemy.orm
from phiphi.api.projects import crud as project_crud
from phiphi.api.projects.gathers import models as gather_model
from phiphi.api.projects.gathers import schemas as gather_schema

# Define a generic type T
response_schema_type = TypeVar(
    "response_schema_type", bound=gather_schema.GatherResponse
)  # Response schema
create_schema_type = TypeVar(
    "create_schema_type", bound=gather_schema.GatherCreate
)  # Create schema
child_model_type = TypeVar("child_model_type", bound=gather_model.Gather)  # child model


def create_child_gather(
    response_schema: Type[response_schema_type],
    session: sqlalchemy.orm.Session,
    project_id: int,
    request_schema: create_schema_type,
    child_model: Type[child_model_type],
) -> response_schema_type:
    """Create child gather."""
    project_crud.get_db_project_with_guard(session, project_id)

    source, platform, data_type = (
        request_schema.source,
        request_schema.platform,
        request_schema.data_type,
    )

    child_type = f"{source.value}_{platform.value}_{data_type.value}"

    db_apify_facebook_post_gather = child_model(
        **request_schema.dict(),
        project_id=project_id,
        child_type=child_type,
    )
    session.add(db_apify_facebook_post_gather)
    session.commit()
    session.refresh(db_apify_facebook_post_gather)
    return response_schema.model_validate(db_apify_facebook_post_gather)
