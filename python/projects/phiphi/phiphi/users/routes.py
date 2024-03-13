"""Routes for the users."""
import fastapi
import sqlalchemy

from phiphi.core import db
from phiphi.users import crud, schemas

router = fastapi.APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, session: sqlalchemy.orm.Session = fastapi.Depends(db.get_session)
) -> schemas.User:
    """Create a new user."""
    return crud.create_user(session, user)
