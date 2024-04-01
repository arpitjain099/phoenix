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
