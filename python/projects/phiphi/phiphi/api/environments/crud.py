"""Environment crud functionality."""
import sqlalchemy.orm
from phiphi.api import utility
from phiphi.api.environments import models, schemas


def create_environment(
    session: sqlalchemy.orm.Session, environment: schemas.EnvironmentCreate
) -> schemas.EnvironmentResponse:
    """Create a new environment."""
    environment_exist = (
        session.query(models.Environment)
        .filter(models.Environment.name == environment.name)
        .first()
    )

    if environment_exist:
        environment_unique_id = utility.generate_random_string(4)
        unique_id = "{}-{}".format(environment.name, environment_unique_id)

    else:
        unique_id = environment.name

    db_environment = models.Environment(**environment.dict(), unique_id=unique_id)
    session.add(db_environment)
    session.commit()
    session.refresh(db_environment)
    return schemas.EnvironmentResponse.model_validate(db_environment)


def get_environment(
    session: sqlalchemy.orm.Session, environment_id: int
) -> schemas.EnvironmentResponse | None:
    """Get an environment."""
    db_environment = session.get(models.Environment, environment_id)
    if db_environment is None:
        return None
    return schemas.EnvironmentResponse.model_validate(db_environment)


def get_environment_by_unique_id(
    session: sqlalchemy.orm.Session, unique_id: str
) -> schemas.EnvironmentResponse | None:
    """Get an environment."""
    print("started")
    db_environment = (
        session.query(models.Environment).filter(models.Environment.unique_id == unique_id).first()
    )
    if db_environment is None:
        return None
    return schemas.EnvironmentResponse.model_validate(db_environment)


def get_environments(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.EnvironmentResponse]:
    """Get environments."""
    query = sqlalchemy.select(models.Environment).offset(start).limit(end)
    environments = session.scalars(query).all()
    if not environments:
        return []
    return [
        schemas.EnvironmentResponse.model_validate(environment) for environment in environments
    ]


def update_environment(
    session: sqlalchemy.orm.Session, environment_id: int, environment: schemas.EnvironmentUpdate
) -> schemas.EnvironmentResponse | None:
    """Update an environment."""
    db_environment = session.get(models.Environment, environment_id)
    if db_environment is None:
        return None
    for field, value in environment.dict(exclude_unset=True).items():
        setattr(db_environment, field, value)
    session.commit()
    session.refresh(db_environment)
    return schemas.EnvironmentResponse.model_validate(db_environment)


def delete_environment(session: sqlalchemy.orm.Session, environment_id: int) -> object:
    """Delete an environment."""
    db_environment = session.get(models.Environment, environment_id)
    if db_environment is None:
        return None
    session.delete(db_environment)
    session.commit()
    ## since there's no generic response, I'm returning an object
    return {"ok": True}
