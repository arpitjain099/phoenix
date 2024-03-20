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


@router.get("/users/", response_model=list[schemas.User])
def read_users(session: api.SessionDep, start: int = 0, end: int = 100) -> list[schemas.User]:
    """Retrieve users."""
    return crud.read_users(session, start, end)


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, session: api.SessionDep) -> schemas.User:
    """Update a user."""
    updated_user = crud.update_user(session, user_id, user)
    if updated_user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return updated_user
