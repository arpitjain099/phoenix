"""Gather crud functionality."""
import sqlalchemy.orm
from phiphi.api import exceptions
from phiphi.api.projects import crud as project_crud
from phiphi.api.projects.gathers import models, schemas


def get_gather(
    session: sqlalchemy.orm.Session, project_id: int, gather_id: int
) -> schemas.GatherResponse | None:
    """Get an apify gather."""
    project_crud.get_db_project_with_guard(session, project_id)

    db_gather = (
        session.query(models.Gather)
        .filter(
            models.Gather.deleted_at.is_(None),
            models.Gather.project_id == project_id,
            models.Gather.id == gather_id,
        )
        .first()
    )
    if db_gather is None:
        return None
    return schemas.GatherResponse.model_validate(db_gather)


## Issues with this implementation
def get_gathers(
    session: sqlalchemy.orm.Session, project_id: int, start: int = 0, end: int = 100
) -> list[schemas.GatherResponse]:
    """Retrieve all gathers and relations.

    Currently this implementation only supports ApifyGathers.
    When new polymorphic model are needed this should be refactored.
    """
    project_crud.get_db_project_with_guard(session, project_id)

    gathers = (
        session.query(models.Gather)
        .filter(models.Gather.project_id == project_id)
        .options(
            # Add additional relationships to be eagerly loaded here
            # Example: joinedload(Gather.other_related_model),
        )
        .slice(start, end)
        .all()
    )

    if not gathers:
        return []
    return [schemas.GatherResponse.model_validate(gather) for gather in gathers]


def get_db_gather_with_guard(
    session: sqlalchemy.orm.Session, project_id: int, gather_id: int
) -> None:
    """Guard for checking if a gather is in the db."""
    db_gather = (
        session.query(models.Gather)
        .filter(models.Gather.project_id == project_id, models.Gather.id == gather_id)
        .first()
    )
    if db_gather is None:
        raise exceptions.GatherNotFound()
