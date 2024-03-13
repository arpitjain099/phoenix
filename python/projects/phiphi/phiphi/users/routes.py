"""Routes for the users."""
import fastapi

from phiphi.core import api
from phiphi.users import crud, schemas

router = fastapi.APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, session: api.SessionDep) -> schemas.User:
    """Create a new user."""
    return crud.create_user(session, user)


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, session: api.SessionDep) -> schemas.User:
    """Read a user."""
    user = crud.read_user(session, user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user
