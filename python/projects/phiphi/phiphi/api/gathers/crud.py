"""Gather crud functionality."""
import json

import sqlalchemy.orm
from phiphi.api.gathers import models, schemas


def apify_map_from_model_to_schema(
    db_apify_gather: models.ApifyGather,
) -> schemas.ApifyGatherResponse:
    """Map an apify gather from model to schema."""
    dict_model = db_apify_gather.__dict__
    dict_model["input_data"] = json.loads(dict_model["input_data"])
    return schemas.ApifyGatherResponse.model_validate(dict_model)


def create_apify_gather(
    session: sqlalchemy.orm.Session, gather_data: schemas.ApifyGatherCreate
) -> schemas.ApifyGatherResponse:
    """Create a new apify gather."""
    dict_gather = gather_data.dict()
    dict_gather["input_data"] = json.dumps(dict_gather["input_data"])
    db_apify_gather = models.ApifyGather(**dict_gather)
    session.add(db_apify_gather)
    session.commit()
    session.refresh(db_apify_gather)
    return apify_map_from_model_to_schema(db_apify_gather)


def get_apify_gather(
    session: sqlalchemy.orm.Session, gather_id: int
) -> schemas.ApifyGatherResponse | None:
    """Get an apify gather."""
    db_gather = session.get(models.ApifyGather, gather_id)
    if db_gather is None:
        return None
    return apify_map_from_model_to_schema(db_gather)


def get_apify_gathers(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Retrieve apify gathers.

    Currently this implementation only supports ApifyGathers.
    When new polymorphic model are needed this should be refactored.
    """
    query = sqlalchemy.select(models.ApifyGather).offset(start).limit(end)
    apify_gathers = session.scalars(query).all()
    if not apify_gathers:
        return []
    return [apify_map_from_model_to_schema(gather) for gather in apify_gathers]


def update_apify_gather(
    session: sqlalchemy.orm.Session, gather_id: int, gather: schemas.ApifyGatherUpdate
) -> schemas.ApifyGatherResponse | None:
    """Update an apify gather."""
    db_gather = session.get(models.ApifyGather, gather_id)
    if db_gather is None:
        return None
    for field, value in gather.dict(exclude_unset=True).items():
        setattr(db_gather, field, value)
    session.commit()
    session.refresh(db_gather)
    return apify_map_from_model_to_schema(db_gather)


## Issues with this implementation
def get_gathers(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Retrieve all gathers and relations.

    Currently this implementation only supports ApifyGathers.
    When new polymorphic model are needed this should be refactored.
    """
    gathers = (
        session.query(models.Gather)
        .options(
            sqlalchemy.orm.joinedload(models.Gather.apify_gather)
            # Add additional relationships to be eagerly loaded here
            # Example: joinedload(Gather.other_related_model),
        )
        .slice(start, end)
        .all()
    )

    if not gathers:
        return []
    return [apify_map_from_model_to_schema(gather) for gather in gathers]
