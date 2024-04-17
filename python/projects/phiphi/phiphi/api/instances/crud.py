"""Instance crud functionality."""
import sqlalchemy.orm

from phiphi.api import exceptions
from phiphi.api.environments import models as env_models
from phiphi.api.instances import models, schemas


def create_instance(
    session: sqlalchemy.orm.Session, instance: schemas.InstanceCreate
) -> schemas.InstanceResponse:
    """Create a new instance."""
    db_environment = (
        session.query(env_models.Environment)
        .filter(env_models.Environment.slug == instance.environment_slug)
        .first()
    )

    if db_environment is None:
        raise exceptions.EnvironmentNotFound()

    db_instance = models.Instance(**instance.dict())
    session.add(db_instance)
    session.commit()
    session.refresh(db_instance)
    return schemas.InstanceResponse.model_validate(db_instance)


def update_instance(
    session: sqlalchemy.orm.Session, instance_id: int, instance: schemas.InstanceUpdate
) -> schemas.InstanceResponse | None:
    """Update an instance."""
    db_instance = session.get(models.Instance, instance_id)
    if db_instance is None:
        return None
    for field, value in instance.dict(exclude_unset=True).items():
        setattr(db_instance, field, value)
    session.commit()
    session.refresh(db_instance)
    return schemas.InstanceResponse.model_validate(db_instance)


def get_instance(
    session: sqlalchemy.orm.Session, instance_id: int
) -> schemas.InstanceResponse | None:
    """Get an instance."""
    db_instance = session.get(models.Instance, instance_id)
    if db_instance is None:
        return None
    return schemas.InstanceResponse.model_validate(db_instance)


def get_instances(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.InstanceResponse]:
    """Get instances."""
    query = sqlalchemy.select(models.Instance).offset(start).limit(end)
    instances = session.scalars(query).all()
    if not instances:
        return []
    return [schemas.InstanceResponse.model_validate(instance) for instance in instances]


def get_db_instance_with_guard(session: sqlalchemy.orm.Session, instance_id: int) -> None:
    """Guard for null instnaces."""
    db_instance = session.query(models.Instance).filter(models.Instance.id == instance_id).first()
    if db_instance is None:
        raise exceptions.InstanceNotFound()
