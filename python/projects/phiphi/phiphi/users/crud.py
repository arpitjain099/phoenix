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
