"""User crud functionality."""
import sqlalchemy.orm

from phiphi.users import models, schemas


def create_user(session: sqlalchemy.orm.Session, user: schemas.UserCreate) -> schemas.User:
    """Create a new user."""
    db_user = models.User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return schemas.User.model_validate(db_user)


def read_user(session: sqlalchemy.orm.Session, user_id: int) -> schemas.User | None:
    """Read a user."""
    db_user = session.get(models.User, user_id)
    if db_user is None:
        return None
    return schemas.User.model_validate(db_user)


def read_users(
    session: sqlalchemy.orm.Session, start: int = 0, end: int = 100
) -> list[schemas.User]:
    """Retrieve users."""
    query = sqlalchemy.select(models.User).offset(start).limit(end)
    users = session.scalars(query).all()
    if not users:
        return []
    return [schemas.User.model_validate(user) for user in users]


def get_user_by_email(session: sqlalchemy.orm.Session, email: str) -> schemas.User | None:
    """Retrieve a user by email."""
    db_user = session.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        return None
    return schemas.User.model_validate(db_user)


def update_user(
    session: sqlalchemy.orm.Session, user_id: int, user: schemas.UserUpdate
) -> schemas.User | None:
    """Update a user."""
    db_user = session.get(models.User, user_id)
    if db_user is None:
        return None
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    session.commit()
    session.refresh(db_user)
    return schemas.User.model_validate(db_user)
