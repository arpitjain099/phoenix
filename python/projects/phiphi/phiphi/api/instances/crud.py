"""Instance crud functionality."""
import sqlalchemy.orm
from phiphi.api.instances import models, schemas


def create_instance(
    session: sqlalchemy.orm.Session, instance: schemas.InstanceCreate
) -> schemas.Instance:
    """Create a new user."""
    if not instance.environment_key:
        instance.environment_key = "main"
    db_instance = models.Instance(**instance.dict())
    session.add(db_instance)
    session.commit()
    session.refresh(db_instance)
    return schemas.Instance.model_validate(db_instance)


def update_instance(
    session: sqlalchemy.orm.Session, instance_id: int, instance: schemas.InstanceUpdate
) -> schemas.Instance | None:
    """Update an instance."""
    db_instance = session.get(models.Instance, instance_id)
    if db_instance is None:
        return None
    for field, value in instance.dict(exclude_unset=True).items():
        setattr(db_instance, field, value)
    session.commit()
    session.refresh(db_instance)
    return schemas.Instance.model_validate(db_instance)


def get_instance(session: sqlalchemy.orm.Session, instance_id: int) -> schemas.Instance | None:
    """Get an instance."""
    db_instance = session.get(models.Instance, instance_id)
    if db_instance is None:
        return None
    return schemas.Instance.model_validate(db_instance)
