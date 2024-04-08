"""Instance crud functionality."""
import sqlalchemy.orm

from phiphi.api.instances import models, schemas


def create_instance(
    session: sqlalchemy.orm.Session, instance: schemas.InstanceCreate
) -> schemas.InstanceResponse:
    """Create a new instance."""
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
