"""Instance runs crud functionality."""
import datetime

import sqlalchemy.orm
from phiphi.api import exceptions
from phiphi.api.instances import crud
from phiphi.api.instances import models as instance_models
from phiphi.api.instances.instance_runs import models, schemas


def create_instance_runs(
    session: sqlalchemy.orm.Session, instance_id: int
) -> schemas.InstanceRunsResponse:
    """Create a new instance run."""
    db_instance = (
        session.query(instance_models.Instance)
        .filter(instance_models.Instance.id == instance_id)
        .first()
    )

    if db_instance is None:
        raise exceptions.InstanceNotFound()

    db_instance_runs = models.InstanceRuns(
        environment_slug=db_instance.environment_slug,
        instance_id=instance_id,
        started_processing_at=datetime.datetime.now(),
    )

    session.add(db_instance_runs)

    session.commit()
    session.refresh(db_instance_runs)
    return schemas.InstanceRunsResponse.model_validate(db_instance_runs)


def get_instance_runs(
    session: sqlalchemy.orm.Session, instance_id: int, start: int = 0, end: int = 100
) -> list[schemas.InstanceRunsResponse]:
    """Get all instance runs."""
    crud.get_db_instance_with_guard(session, instance_id)

    query = (
        sqlalchemy.select(models.InstanceRuns)
        .filter(models.InstanceRuns.instance_id == instance_id)
        .offset(start)
        .limit(end)
    )
    db_instance_runs = session.scalars(query).all()

    if not db_instance_runs:
        return []
    return [schemas.InstanceRunsResponse.model_validate(runs) for runs in db_instance_runs]


def get_instance_last_run(
    session: sqlalchemy.orm.Session, instance_id: int
) -> schemas.InstanceRunsResponse | None:
    """Get last instance run."""
    crud.get_db_instance_with_guard(session, instance_id)

    db_instance_run = (
        session.query(models.InstanceRuns)
        .filter(models.InstanceRuns.instance_id == instance_id)
        .order_by(models.InstanceRuns.created_at.desc())
        .first()
    )

    if db_instance_run is None:
        return None
    return schemas.InstanceRunsResponse.model_validate(db_instance_run)
