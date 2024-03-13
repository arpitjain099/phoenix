"""Routes for the users."""
import fastapi

from phiphi.core import api
from phiphi.users import crud, schemas

router = fastapi.APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, session: api.SessionDep) -> schemas.User:
    """Create a new user."""
    return crud.create_user(session, user)
