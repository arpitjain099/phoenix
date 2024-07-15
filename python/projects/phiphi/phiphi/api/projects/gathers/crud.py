"""Gather crud functionality."""
import sqlalchemy.orm

from phiphi.api import exceptions
from phiphi.api.projects import crud as project_crud
from phiphi.api.projects.gathers import models, schemas
from phiphi.api.projects.job_runs import crud as job_run_crud
from phiphi.api.projects.job_runs import schemas as job_run_schemas


def get_gather(
    session: sqlalchemy.orm.Session, project_id: int, gather_id: int
) -> schemas.GatherResponse | None:
    """Get an apify gather."""
    db_gather = get_db_gather(session, project_id, gather_id)
    if db_gather is None:
        return None
    return schemas.GatherResponse.model_validate(db_gather)


def get_db_gather(
    session: sqlalchemy.orm.Session, project_id: int, gather_id: int
) -> models.Gather | None:
    """Get a gather orm model."""
    project_crud.get_db_project_with_guard(session, project_id)
    db_gather = (
        session.query(models.Gather)
        .filter(
            models.Gather.project_id == project_id,
            models.Gather.id == gather_id,
        )
        .first()
    )
    return db_gather


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


async def delete(
    session: sqlalchemy.orm.Session, project_id: int, gather_id: int
) -> schemas.GatherResponse:
    """Delete a gather."""
    db_gather = get_db_gather(session, project_id, gather_id)
    if db_gather is None:
        raise exceptions.GatherNotFound()

    delete_job_run_response = await job_run_crud.create_and_run_job_run(
        session,
        project_id,
        job_run_schemas.JobRunCreate(
            foreign_id=gather_id,
            foreign_job_type=job_run_schemas.ForeignJobType.gather_delete,
        ),
    )

    db_gather.delete_job_run_id = delete_job_run_response.id
    session.commit()
    return schemas.GatherResponse.model_validate(db_gather)
