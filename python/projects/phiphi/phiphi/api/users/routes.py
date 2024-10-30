"""Routes for the users."""
import fastapi

from phiphi.api import deps
from phiphi.api.users import crud, schemas

router = fastapi.APIRouter()


# It is important that this route is defined before the /users/{user_id} route or me will be
# interpreted as a user id
@router.get("/users/me", response_model=schemas.UserResponse)
def read_me(current_user: deps.CurrentUser) -> schemas.UserResponse:
    """Get the current users."""
    return current_user


@router.post("/users/", response_model=schemas.UserResponse)
def create_user(
    admin_user: deps.AdminOnlyUser, user: schemas.UserCreate, session: deps.SessionDep
) -> schemas.UserResponse:
    """Create a new user."""
    return crud.create_user(session, user)


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, session: deps.SessionDep) -> schemas.UserResponse:
    """Read a user."""
    user = crud.read_user(session, user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=list[schemas.UserResponse])
def read_users(
    session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.UserResponse]:
    """Retrieve users."""
    return crud.read_users(session, start, end)


@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int, user: schemas.UserUpdate, session: deps.SessionDep
) -> schemas.UserResponse:
    """Update a user."""
    updated_user = crud.update_user(session, user_id, user)
    if updated_user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return updated_user
