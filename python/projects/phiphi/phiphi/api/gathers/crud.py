"""Gather crud functionality."""
import sqlalchemy.orm
from phiphi.api.gathers import models, schemas


def create_apify_gather(
    session: sqlalchemy.orm.Session, gather_data: schemas.ApifyGatherCreate
) -> schemas.ApifyGatherResponse:
    """Create a new apify gather."""
    db_apify_gather = models.ApifyGather(**gather_data.dict())
    session.add(db_apify_gather)
    session.commit()
    session.refresh(db_apify_gather)
    return schemas.ApifyGatherResponse.model_validate(db_apify_gather)


def get_apify_gather(
    session: sqlalchemy.orm.Session, gather_id: int
) -> schemas.ApifyGatherResponse | None:
    """Get an apify gather."""
    db_gather = session.get(models.ApifyGather, gather_id)
    if db_gather is None:
        return None
    return schemas.ApifyGatherResponse.model_validate(db_gather)


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
    return [schemas.ApifyGatherResponse.model_validate(gather) for gather in apify_gathers]


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
            # Add additional relationships to be eagerly loaded here
            # Example: joinedload(Gather.other_related_model),
        )
        .slice(start, end)
        .all()
    )

    if not gathers:
        return []
    return [schemas.ApifyGatherResponse.model_validate(gather) for gather in gathers]
