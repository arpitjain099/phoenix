"""Environment crud functionality."""
import slugify
import sqlalchemy.orm
from phiphi.api import utility
from phiphi.api.environments import models, schemas


def create_environment(
    session: sqlalchemy.orm.Session, environment: schemas.EnvironmentCreate
) -> schemas.EnvironmentResponse:
    """Create a new environment."""
    slug_exist = (
        session.query(models.Environment)
        .filter(models.Environment.slug == environment.slug)
        .first()
    )

    if slug_exist:
        raise Exception("Slug already exists")

    environment.name = slugify.slugify(environment.name)
    db_environment = models.Environment(**environment.dict())
    session.add(db_environment)
    session.commit()
    session.refresh(db_environment)
    return schemas.EnvironmentResponse.model_validate(db_environment)


def get_environment(
    session: sqlalchemy.orm.Session, slug: str
) -> schemas.EnvironmentResponse | None:
    """Get an environment."""
    db_environment = (
        session.query(models.Environment).filter(models.Environment.slug == slug).first()
    )

    if db_environment is None:
        return None
    return schemas.EnvironmentResponse.model_validate(db_environment)


def get_environment_by_slug(
    session: sqlalchemy.orm.Session, slug: str
) -> schemas.EnvironmentResponse | None:
    """Get an environment."""
    print("started")
    db_environment = (
        session.query(models.Environment).filter(models.Environment.slug == slug).first()
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


def get_unique_slug(
    session: sqlalchemy.orm.Session, environment_name: str
) -> schemas.SlugResponse:
    """Get unique slug."""
    slug_exist = (
        session.query(models.Environment)
        .filter(models.Environment.slug == environment_name)
        .first()
    )

    name = slugify.slugify(environment_name)
    print(name)
    if slug_exist:
        random_str = utility.generate_random_string(4)
        slug = "{}-{}".format(name, random_str)

    else:
        slug = name

    response = schemas.SlugResponse(slug=slug)

    print(response)
    return schemas.SlugResponse.model_validate(response)
