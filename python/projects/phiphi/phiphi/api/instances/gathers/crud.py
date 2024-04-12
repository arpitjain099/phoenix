"""Gather crud functionality."""
import sqlalchemy.orm
from phiphi.api.instances import models as instance_models
from phiphi.api.instances.gathers import models, schemas
from phiphi.exceptions import instance_not_found


def create_apify_gather(
    session: sqlalchemy.orm.Session, instance_id: int, gather_data: schemas.ApifyGatherCreate
) -> schemas.ApifyGatherResponse:
    """Create a new apify gather."""
    db_instance = (
        session.query(instance_models.Instance)
        .filter(instance_models.Instance.id == instance_id)
        .first()
    )
    if db_instance is None:
        raise instance_not_found.InstanceNotFound()

    db_apify_gather = models.ApifyGather(**gather_data.dict(), instance_id=instance_id)
    session.add(db_apify_gather)
    session.commit()
    session.refresh(db_apify_gather)
    return schemas.ApifyGatherResponse.model_validate(db_apify_gather)


def get_apify_gather(
    session: sqlalchemy.orm.Session, instance_id: int, gather_id: int
) -> schemas.ApifyGatherResponse | None:
    """Get an apify gather."""
    db_instance = (
        session.query(instance_models.Instance)
        .filter(instance_models.Instance.id == instance_id)
        .first()
    )
    if db_instance is None:
        raise instance_not_found.InstanceNotFound()

    db_gather = (
        session.query(models.ApifyGather)
        .filter(
            models.ApifyGather.deleted_at.is_(None),
            models.ApifyGather.instance_id == instance_id,
            models.ApifyGather.id == gather_id,
        )
        .first()
    )
    if db_gather is None:
        return None
    return schemas.ApifyGatherResponse.model_validate(db_gather)


def get_apify_gathers(
    session: sqlalchemy.orm.Session, instance_id: int, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Retrieve apify gathers.

    Currently this implementation only supports ApifyGathers.
    When new polymorphic model are needed this should be refactored.
    """
    db_instance = (
        session.query(instance_models.Instance)
        .filter(instance_models.Instance.id == instance_id)
        .first()
    )
    if db_instance is None:
        raise instance_not_found.InstanceNotFound()

    query = (
        sqlalchemy.select(models.ApifyGather)
        .filter(
            models.ApifyGather.deleted_at.is_(None), models.ApifyGather.instance_id == instance_id
        )
        .offset(start)
        .limit(end)
    )
    apify_gathers = session.scalars(query).all()
    if not apify_gathers:
        return []
    return [schemas.ApifyGatherResponse.model_validate(gather) for gather in apify_gathers]


## Issues with this implementation
def get_gathers(
    session: sqlalchemy.orm.Session, instance_id: int, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Retrieve all gathers and relations.

    Currently this implementation only supports ApifyGathers.
    When new polymorphic model are needed this should be refactored.
    """
    db_instance = (
        session.query(instance_models.Instance)
        .filter(instance_models.Instance.id == instance_id)
        .first()
    )
    if db_instance is None:
        raise instance_not_found.InstanceNotFound()

    gathers = (
        session.query(models.Gather)
        .filter(models.Gather.instance_id == instance_id)
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
